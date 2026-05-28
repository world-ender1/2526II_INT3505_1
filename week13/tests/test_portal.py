from pathlib import Path

from app import create_app


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "static" / "styles.css").read_text(encoding="utf-8")
JS = (ROOT / "static" / "app.js").read_text(encoding="utf-8")


def test_home_route_renders_developer_portal():
    app = create_app()
    app.config.update(TESTING=True)

    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"EduLibrary API Developer Portal" in response.data
    assert b"/static/styles.css" in response.data
    assert b"/static/app.js" in response.data


def test_developer_portal_includes_required_sitemap_sections():
    required_sections = [
        'id="home"',
        'id="quickstart"',
        'id="reference"',
        'id="sandbox"',
        'id="pricing"',
        'id="analytics"',
        'id="changelog"',
        'id="support"',
    ]

    for section in required_sections:
        assert section in TEMPLATE


def test_business_model_canvas_covers_core_model_blocks_from_plan():
    required_blocks = [
        "Customer Segments",
        "Value Propositions",
        "Channels",
        "Customer Relationships",
        "Revenue Streams",
        "Key Resources",
    ]

    for block in required_blocks:
        assert block in TEMPLATE


def test_portal_documents_monetization_tiers_and_kpi_analytics():
    for tier in ["Free", "Pro", "Business", "Enterprise"]:
        assert f">{tier}<" in TEMPLATE

    for kpi in ["Developer signups", "Call volume", "Error rate", "Latency p95"]:
        assert kpi in TEMPLATE


def test_api_reference_includes_crud_book_endpoints():
    endpoint_checks = [
        "GET</code></td><td><code>/v1/books</code>",
        "GET</code></td><td><code>/v1/books/{id}</code>",
        "POST</code></td><td><code>/v1/books</code>",
        "PATCH</code></td><td><code>/v1/books/{id}</code>",
        "DELETE</code></td><td><code>/v1/books/{id}</code>",
    ]

    for endpoint in endpoint_checks:
        assert endpoint in TEMPLATE


def test_sandbox_has_sample_key_and_copy_behavior():
    assert "el_sandbox_sample_key" in TEMPLATE
    assert 'id="copy-key"' in TEMPLATE
    assert "navigator.clipboard.writeText" in JS


def test_responsive_css_exists_for_mobile_layouts():
    assert "@media (max-width: 900px)" in CSS
    assert "grid-template-columns: 1fr" in CSS
