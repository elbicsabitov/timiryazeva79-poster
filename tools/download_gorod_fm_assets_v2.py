"""Download all v2 Figma assets for Город ФМ pixel-perfect rebuild.

Each entry maps a descriptive ASCII filename to the ephemeral Figma MCP asset URL
fetched 2026-05-27 night. URLs expire ~7 days after fetch.
"""
from __future__ import annotations
import pathlib
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = pathlib.Path(__file__).resolve().parents[1] / "designs" / "assets" / "gorod-fm"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ASSETS: dict[str, str] = {
    # === Shared UI icons (use one canonical copy per semantic icon) ===
    "ui-icon-search.png": "https://www.figma.com/api/mcp/asset/f5c2e2a8-b4b9-4d55-adce-5a8f0319c0b6",
    "ui-icon-music-artist.png": "https://www.figma.com/api/mcp/asset/2aa44727-11fc-4fa4-b719-74422460a02a",
    "ui-icon-podcast.png": "https://www.figma.com/api/mcp/asset/9d691439-4ed3-4121-89b9-f619197d0025",
    "ui-icon-media.png": "https://www.figma.com/api/mcp/asset/ad417070-8a70-466e-862e-180fa85751fb",
    "ui-icon-star.png": "https://www.figma.com/api/mcp/asset/6bf44135-94fe-4303-8aa4-741746f1edae",
    "ui-icon-skip-back.png": "https://www.figma.com/api/mcp/asset/17d7dc33-9e02-493f-b514-8b69ae57c6de",
    "ui-icon-play.png": "https://www.figma.com/api/mcp/asset/956d3db4-b52c-4c78-9916-adbb73e9a2b3",
    "ui-icon-skip-forward.png": "https://www.figma.com/api/mcp/asset/4e8329cc-fdfe-45a0-805c-f87f8f0200b2",
    "ui-icon-share.png": "https://www.figma.com/api/mcp/asset/cd3dfce5-6b6e-4bd0-bd4e-a1c82d55df13",
    "ui-icon-volume.png": "https://www.figma.com/api/mcp/asset/964b3413-72eb-4033-bd10-fa1abd433925",
    "ui-volume-slider.png": "https://www.figma.com/api/mcp/asset/ec7f43c1-b3cc-4b97-8244-04f142366fd0",
    "ui-icon-play-arrow.png": "https://www.figma.com/api/mcp/asset/2f24c6f7-3972-4f83-9162-c2b96f55ef66",
    "ui-arrow-right.png": "https://www.figma.com/api/mcp/asset/e0b77c47-803d-4232-8f0d-12ca529e44a7",
    "ui-arrow-down.png": "https://www.figma.com/api/mcp/asset/4a7d91b1-99e2-4e57-9d3d-de13ffc34c85",
    "ui-line-divider.png": "https://www.figma.com/api/mcp/asset/85991457-5460-4b76-b5ba-8a709ffbd3f7",
    "ui-dot.png": "https://www.figma.com/api/mcp/asset/9faa2147-2849-4300-9661-9186f38da9b5",
    "ui-volume-slider-tracks.png": "https://www.figma.com/api/mcp/asset/26dd752c-7fe1-4c9a-8f1c-547068038b82",
    "ui-social-whatsapp.png": "https://www.figma.com/api/mcp/asset/f9958c0f-b71a-4c48-86a3-e8bb4724f4c1",
    "ui-social-telegram.png": "https://www.figma.com/api/mcp/asset/f8628657-0da3-4b63-8370-3305605ac93a",
    "ui-social-vk.png": "https://www.figma.com/api/mcp/asset/6bd60bb0-ed93-445e-b53e-97941fd2e80a",
    "ui-icon-fav-heart.png": "https://www.figma.com/api/mcp/asset/22ec5dc4-a116-41f9-a048-a5a91f58bd6d",
    "ui-icon-options.png": "https://www.figma.com/api/mcp/asset/0fc0a4b8-0bc9-4c4f-aaa3-4136874a2755",

    # === Home 2174:422 ===
    "home-bg-particles.png": "https://www.figma.com/api/mcp/asset/c6f2f2bb-d78a-41e7-877a-e2aedc939d34",
    "home-tile-dfm-chill-far.png": "https://www.figma.com/api/mcp/asset/ee9f55cd-f8ee-408e-98c3-a888c68d41a5",
    "home-tile-vadim-adamov-base.png": "https://www.figma.com/api/mcp/asset/74eeaf5c-9618-4d65-b51e-1e5ee6c2ae62",
    "home-tile-vadim-adamov-overlay.png": "https://www.figma.com/api/mcp/asset/5d63576a-b039-411f-9997-4e02a2d8c76b",
    "home-tile-z-city-show.png": "https://www.figma.com/api/mcp/asset/5ef713f7-dab7-4e58-9b5b-fada2b121812",
    "home-tile-discach-90.png": "https://www.figma.com/api/mcp/asset/64573bc2-f8c2-49ac-8bc8-2334b6bdc257",
    "home-tile-chill.png": "https://www.figma.com/api/mcp/asset/db59ca6e-7755-4797-9a74-a76c1898e52e",
    "home-tile-k-pop.png": "https://www.figma.com/api/mcp/asset/e5c08b01-57ba-4ae3-b82d-b98edeffb577",
    "home-tile-pop-gold-2010s.png": "https://www.figma.com/api/mcp/asset/32efd4b8-0625-4ca9-a9b5-991ac73e65c1",
    "home-featured-egor-krid.png": "https://www.figma.com/api/mcp/asset/271dfcf3-4643-4bcd-891c-260bd9e6de0d",
    "home-now-playing.png": "https://www.figma.com/api/mcp/asset/19e27cce-ace9-4e4a-b20f-d09c3743bf8b",

    # === Подборки 2384:6054 ===
    "podborki-now-playing.png": "https://www.figma.com/api/mcp/asset/fe262757-7811-4fc6-880c-19e6ce6a133f",
    "podborki-tile-dfm-chill-base.png": "https://www.figma.com/api/mcp/asset/99588c8c-2c72-410b-9070-b9493c6e0937",
    "podborki-tile-dfm-chill-overlay.png": "https://www.figma.com/api/mcp/asset/ff3943e8-15e7-4a65-906f-45f0cff2ce6b",
    "podborki-tile-dj-pitkin.png": "https://www.figma.com/api/mcp/asset/a8313600-8030-4e69-b156-781f22b10ab0",
    "podborki-tile-vadim-adamov.png": "https://www.figma.com/api/mcp/asset/25d9113a-4198-40b2-855b-382089056055",
    "podborki-tile-z-city-show.png": "https://www.figma.com/api/mcp/asset/e0d2d916-cf23-40bc-8c4a-38c6fcb99a83",
    "podborki-tile-discach-90.png": "https://www.figma.com/api/mcp/asset/a58d3ca8-dbb3-4685-af61-1cbf4732af6a",
    "podborki-tile-chill.png": "https://www.figma.com/api/mcp/asset/72b1b688-4af3-40f0-8887-45382b275ba5",
    "podborki-tile-k-pop.png": "https://www.figma.com/api/mcp/asset/f75ff2ab-0c55-4ce5-9cc0-4d5fc2ca6ab7",
    "podborki-tile-pop-gold-2010s.png": "https://www.figma.com/api/mcp/asset/b6da2d7e-d598-4a90-867f-cccdc9d0dde1",

    # === Медиатека 2385:2924 — А-row 18 artists ===
    "library-artist-arthur-pirozhkov.png": "https://www.figma.com/api/mcp/asset/113fdf63-8ce2-4451-956d-a721c8e6ee97",
    "library-artist-ariya.png": "https://www.figma.com/api/mcp/asset/f4ae37cd-0f6f-4514-94ff-70f775782b0e",
    "library-artist-alisa.png": "https://www.figma.com/api/mcp/asset/b48725e0-0e51-4864-9fd1-f1575bda67f2",
    "library-artist-ani-lorak.png": "https://www.figma.com/api/mcp/asset/6df6bfc2-eaa9-49e5-b291-4de7514b9cdf",
    "library-artist-ak-47.png": "https://www.figma.com/api/mcp/asset/464b3077-762c-475e-beef-7a6e5600f54b",
    "library-artist-alsu.png": "https://www.figma.com/api/mcp/asset/63024173-8ab8-4f7e-800a-777143fb61b0",
    "library-artist-anet-sai.png": "https://www.figma.com/api/mcp/asset/cd63604e-9a9f-4ace-9b03-92542c717cb3",
    "library-artist-asia.png": "https://www.figma.com/api/mcp/asset/89fbbeb6-a2d5-4b1e-b66a-979709bef096",
    "library-artist-akvarium.png": "https://www.figma.com/api/mcp/asset/310a767c-591e-4ac9-91b6-6bc1e57db0b6",
    "library-artist-anton-tokarev.png": "https://www.figma.com/api/mcp/asset/4a8b3d67-6a0e-4b70-a7e0-f8fc3fc87860",
    "library-artist-a-studio.png": "https://www.figma.com/api/mcp/asset/18cd441a-d631-458d-9355-374880865836",
    "library-artist-anna-german.png": "https://www.figma.com/api/mcp/asset/e2de1105-970f-4e96-b110-d907d900f691",
    "library-artist-alsmi.png": "https://www.figma.com/api/mcp/asset/4e396b3f-a224-4322-9714-2f2fdf109032",
    "library-artist-aigel.png": "https://www.figma.com/api/mcp/asset/75a2422c-b939-4935-bab9-c0842c0d5851",
    "library-artist-artur.png": "https://www.figma.com/api/mcp/asset/41928f5d-fd5f-428b-9b59-7bc8393fb1b3",
    "library-artist-anna-vorobey.png": "https://www.figma.com/api/mcp/asset/44242a17-9477-4196-8b57-ceea04b1f975",
    "library-artist-afina.png": "https://www.figma.com/api/mcp/asset/e30198e4-b09e-400c-9e71-bc9432e13312",
    "library-artist-alyans.png": "https://www.figma.com/api/mcp/asset/ecc55502-e9ed-47b0-9507-1ab65d4b8d55",

    # === Избранное (раздел) 2535:11151 ===
    # DJ row
    "favs-dj-martin-garrix.png": "https://www.figma.com/api/mcp/asset/ec091ab5-287b-451c-9cf7-ea71aaea0915",
    "favs-dj-2.png": "https://www.figma.com/api/mcp/asset/54ca399e-c68a-450e-b73f-2cb0b232188e",
    "favs-dj-3.png": "https://www.figma.com/api/mcp/asset/8e4c3ffe-e805-4123-afc9-6159c8e03239",
    "favs-dj-4.png": "https://www.figma.com/api/mcp/asset/d11ec7ed-ccbd-4859-9be4-c4f86dd3bb2a",
    "favs-dj-5.png": "https://www.figma.com/api/mcp/asset/f029a497-81f9-4dcb-ab17-806d7b1fb77c",
    "favs-dj-6.png": "https://www.figma.com/api/mcp/asset/ae3025bc-fcfb-440d-9cee-41440817b4a4",
    "favs-dj-7.png": "https://www.figma.com/api/mcp/asset/9f08fe3f-57a4-498e-908c-ba9169a1a5e5",
    # Группы row
    "favs-group-bernhoft.png": "https://www.figma.com/api/mcp/asset/99f14a8e-f162-4873-a479-0dcdc889ed40",
    "favs-group-ludovico-overlay.png": "https://www.figma.com/api/mcp/asset/0202bec7-d2e4-407a-8a36-a1a239a1e853",
    "favs-group-my-darkest-days.png": "https://www.figma.com/api/mcp/asset/afa2c511-35c0-4477-aec4-32def740ed28",
    "favs-group-linkin-park-overlay.png": "https://www.figma.com/api/mcp/asset/461a700e-eae9-4cd2-b583-18f0c68c6385",
    "favs-group-crystal-castles.png": "https://www.figma.com/api/mcp/asset/b8344c50-864c-42a9-b76a-e930d9bc4821",
    "favs-group-ramil.png": "https://www.figma.com/api/mcp/asset/f8bb76fe-e164-4c72-8219-b0583315896b",
    # Исполнители row
    "favs-artist-maks-korzh-base.png": "https://www.figma.com/api/mcp/asset/a249b3d0-297f-4f6f-82e5-e1bf794b8df2",
    "favs-artist-rem-diga-overlay.png": "https://www.figma.com/api/mcp/asset/d6d8f397-81ef-40cf-8b45-9a6365e4971e",
    "favs-artist-ramil.png": "https://www.figma.com/api/mcp/asset/308c4fb5-3ba2-47e9-a6fc-f4e4a827cc9e",
    "favs-artist-akon.png": "https://www.figma.com/api/mcp/asset/eebbcce0-3080-4d74-86d5-e031135d754f",
    "favs-artist-mia-boyka.png": "https://www.figma.com/api/mcp/asset/bb713900-d676-42cf-8333-f4d23c5a7b23",
    "favs-artist-dima-bilan-overlay.png": "https://www.figma.com/api/mcp/asset/c4b6c1a3-c93d-4a8b-8c09-73bb6681db68",

    # === Страница артиста 2537:14090 ===
    "artist-hero-arthur.png": "https://www.figma.com/api/mcp/asset/3fdf0b44-b84e-48ae-8a56-830f4a1dfaad",
    "artist-thumb-arthur-small.png": "https://www.figma.com/api/mcp/asset/c5411fc2-ba03-4253-85e3-d8d0004ea32b",
    "artist-track-cover-base.png": "https://www.figma.com/api/mcp/asset/8a7bde1d-6c44-4519-ad70-8bbb1e488d50",
    "artist-track-cover-sleza.png": "https://www.figma.com/api/mcp/asset/862ea71d-3974-45d1-bd01-56abbac8da5f",
    "artist-track-cover-samolyot.png": "https://www.figma.com/api/mcp/asset/a20eb53a-5c03-4c0b-9344-84dc6a5ccd13",
    "artist-track-cover-druzhelyubny.png": "https://www.figma.com/api/mcp/asset/699465a6-4a9c-40ec-bb13-400af0bf7213",
    "artist-track-cover-budem.png": "https://www.figma.com/api/mcp/asset/ad3ed6ea-94ca-4f69-86e9-d30130e9f8b0",
}


def download(name_url: tuple[str, str]) -> tuple[str, int | str]:
    name, url = name_url
    dst = OUT_DIR / name
    if dst.exists() and dst.stat().st_size > 0:
        return name, "skip-existing"
    req = urllib.request.Request(url, headers={"User-Agent": "gorod-fm-v2/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        dst.write_bytes(data)
        return name, len(data)
    except Exception as e:
        return name, f"ERR {e!r}"


def main() -> int:
    print(f"Downloading {len(ASSETS)} assets to {OUT_DIR}", flush=True)
    failed: list[str] = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = [pool.submit(download, item) for item in ASSETS.items()]
        for fut in as_completed(futures):
            name, result = fut.result()
            print(f"  {name}: {result}", flush=True)
            if isinstance(result, str) and result.startswith("ERR"):
                failed.append(name)
    if failed:
        print(f"\nFAILED ({len(failed)}): {failed}", flush=True)
        return 1
    print(f"\nOK — {len(ASSETS)} files in {OUT_DIR}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
