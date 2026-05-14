from __future__ import annotations

from dataclasses import dataclass

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


class SelectionError(Exception):
    """사용자가 해결할 수 있는 선택/브라우저 오류입니다."""


@dataclass(frozen=True)
class ClickSelection:
    selector: str
    text: str
    tag_name: str


CLICK_SCRIPT = """
({ message, parentDepth }) => {
  return new Promise((resolve) => {
    const oldOverlay = document.getElementById("__jd_extractor_overlay__");
    if (oldOverlay) oldOverlay.remove();

    const overlay = document.createElement("div");
    overlay.id = "__jd_extractor_overlay__";
    overlay.textContent = message;
    Object.assign(overlay.style, {
      position: "fixed",
      top: "16px",
      left: "50%",
      transform: "translateX(-50%)",
      zIndex: "2147483647",
      padding: "12px 16px",
      borderRadius: "8px",
      background: "#111827",
      color: "#ffffff",
      fontSize: "15px",
      fontFamily: "Arial, sans-serif",
      boxShadow: "0 8px 24px rgba(0,0,0,0.24)",
      pointerEvents: "none",
    });
    document.body.appendChild(overlay);

    const previousOutline = new WeakMap();

    function cssEscape(value) {
      if (window.CSS && window.CSS.escape) return window.CSS.escape(value);
      return String(value).replace(/[^a-zA-Z0-9_-]/g, "\\\\$&");
    }

    function restoreOutline(element) {
      if (!element || !previousOutline.has(element)) return;
      element.style.outline = previousOutline.get(element);
      previousOutline.delete(element);
    }

    function highlight(element) {
      if (!previousOutline.has(element)) previousOutline.set(element, element.style.outline);
      element.style.outline = "3px solid #2563eb";
    }

    function selectorFor(element) {
      if (!element || element.nodeType !== Node.ELEMENT_NODE) return "";
      if (element.id) return `#${cssEscape(element.id)}`;

      const parts = [];
      let current = element;

      while (current && current.nodeType === Node.ELEMENT_NODE && current !== document.body) {
        let part = current.nodeName.toLowerCase();

        if (current.classList.length > 0) {
          const classNames = Array.from(current.classList).slice(0, 3).map(cssEscape);
          part += "." + classNames.join(".");
        }

        const parent = current.parentElement;
        if (parent) {
          const sameTagSiblings = Array.from(parent.children).filter(
            (child) => child.nodeName === current.nodeName
          );
          if (sameTagSiblings.length > 1) {
            part += `:nth-of-type(${sameTagSiblings.indexOf(current) + 1})`;
          }
        }

        parts.unshift(part);
        current = parent;
      }

      return parts.join(" > ");
    }

    function expandToParent(element, depth) {
      let current = element;
      for (let i = 0; i < depth; i += 1) {
        if (!current.parentElement || current.parentElement === document.body) break;
        current = current.parentElement;
      }
      return current;
    }

    let lastHovered = null;

    function onMouseOver(event) {
      const target = event.target;
      if (!(target instanceof Element) || target.id === "__jd_extractor_overlay__") return;
      restoreOutline(lastHovered);
      lastHovered = expandToParent(target, parentDepth);
      highlight(lastHovered);
    }

    function onClick(event) {
      event.preventDefault();
      event.stopPropagation();

      let selected = event.target;
      if (!(selected instanceof Element)) return;
      selected = expandToParent(selected, parentDepth);

      document.removeEventListener("mouseover", onMouseOver, true);
      document.removeEventListener("click", onClick, true);
      restoreOutline(lastHovered);
      overlay.remove();

      resolve({
        selector: selectorFor(selected),
        text: (selected.innerText || selected.textContent || "").trim(),
        tagName: selected.tagName.toLowerCase(),
      });
    }

    document.addEventListener("mouseover", onMouseOver, true);
    document.addEventListener("click", onClick, true);
  });
}
"""


def select_job_areas(url: str, title_parent_depth: int = 0, jd_parent_depth: int = 1) -> dict[str, str]:
    """브라우저를 열고 사용자가 클릭한 제목/JD 영역을 추출합니다."""
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page.set_default_timeout(0)

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                except PlaywrightTimeoutError as exc:
                    raise SelectionError("페이지 로딩 시간이 초과되었습니다. URL을 확인하거나 잠시 후 다시 시도하세요.") from exc

                title = _wait_for_click(
                    page,
                    "제목 영역을 클릭하세요. 작은 글자만 잡히면 제목 부모 확장 단계를 올려 다시 선택하세요.",
                    title_parent_depth,
                )
                jd = _wait_for_click(
                    page,
                    "본문/JD 영역을 클릭하세요. 내용이 짧게 잡히면 부모 확장 단계를 올려 다시 선택하세요.",
                    jd_parent_depth,
                )
            finally:
                browser.close()

        return {
            "title": title.text,
            "jd": jd.text,
            "source_url": url,
            "title_selector": title.selector,
            "jd_selector": jd.selector,
        }
    except PlaywrightError as exc:
        raise SelectionError(
            "Playwright 실행 중 오류가 발생했습니다. 브라우저 설치 상태와 URL 접근 가능 여부를 확인하세요."
        ) from exc


def _wait_for_click(page, message: str, parent_depth: int) -> ClickSelection:
    result = page.evaluate(CLICK_SCRIPT, {"message": message, "parentDepth": parent_depth})
    text = (result.get("text") or "").strip()
    if not text:
        raise SelectionError("선택한 영역에서 텍스트를 찾지 못했습니다. 다른 영역을 다시 선택하세요.")

    return ClickSelection(
        selector=result.get("selector") or "",
        text=text,
        tag_name=result.get("tagName") or "",
    )
