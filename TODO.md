# Hackathon UI Upgrade Tasks

## Risk Map Page
- [x] Update `dashboard/views.py` `risk_map` to pass richer context (stats, created_at, image URLs, reports list)
- [x] Redesign `dashboard/templates/dashboard/risk_map.html` with dark-themed hackathon-ready UI:
  - Modern navbar with branding
  - Animated gradient stat cards (High/Medium/Low/Total)
  - Full-height dark map (CartoDB tiles)
  - Leaflet.heat heatmap overlay for risk density
  - Pulsing animated markers for high-risk zones
  - Filter buttons (All/High/Medium/Low)
  - Floating legend panel
  - Reports list side panel with risk badges
  - Glassmorphism effects, smooth animations, responsive
  - Footer

## Report Breeding Spot Page
- [x] Update `dashboard/forms.py` with modern widget styling (Bootstrap classes, placeholders)
- [x] Redesign `dashboard/templates/dashboard/report_form.html`:
  - Attractive hero/header section
  - Interactive map for location picking (click to set lat/lng)
  - Better styled form with icons
  - Success message alerts
  - Steps guide / how-it-works section

## Testing
- [x] Verify `/risk-map/` loads without errors (200 OK)
- [x] Verify `/report/` loads without errors (200 OK)
- [x] Fixed broken Django template tag in report_form.html (broken {% endif %} tag)
- [x] Live server verification — both pages return 200 OK

