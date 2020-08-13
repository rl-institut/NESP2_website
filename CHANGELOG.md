# Changelog
All notable changes to this project will be documented in this file.

The format is inspired from [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and the versioning aim to respect [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

Here is a template for new release sections

```
## [_._._] - 20XX-MM-DD

### Added
-
### Changed
-
### Removed
-
```
## [Unreleased]
### Added
- Popup to warn against unsupported browsers (#183)
- Video popup for `/map` endpoints (#186, #187)
- Video embedded in iframe in the `/about-map` endpoint (#188)
### Changed
- The introductory webmap youtube video's id is provided to the jinja templates from the
 `app/blueprints/maps.py` module (#187)
- Change map url endpoint from `/maps` to `/map` (#185)

### Removed

## [0.2.0] - 2020-03-21

Pre-release version of the NESP website

### Added
- social media links (#74)
- resource content (#75)
- meta tags in header (#78)
- tests of page access (#79)
- build badge to readme (#82)
- connection to postgres database (#85)
- gauge max value is queried from the database (#96)
- all gauges values are queried from the database (#98)
- index.py file (#101)
- objectives route and blueprint (#128)
- links from logo (#129)
- about-map page (#153, #162)
- fadein for features (#155)
- automatic redraw of gauges when scrolling over (#157)
- automatic interval change of feature when section is in viewport (#157)
- link to web development credit page (#157)
- developed-by page (#162)
- licenses (#167)

### Changed
- allow use of variable via URL (#76)
- make table in about responsive and centered (#88)
- dockerfile setup to use postgres (#91)
- OG grid mapping image (#95)
- gauge line is thicker (#96)
- adapt setup_maps.py for windows users (#101)
- the webmap uses its own base template (without header and footer) (#101)
- ratio of giz logos (#129)
- objective cards design (#145)
- images size (#148)
- nigeria se4all section in about page centered with images inline (#154) 
- rename about-map.html credits.html (#162)

### Removed
- app/index.py file (#101)
- outline around the clicked links (#129)
- about-map blueprint (#162)

### Fixed
- chrome display bug #64 for small screens (#86)
- return button was not working (#93)
- mismatching font for gauges numbers #97 (#98)

## [0.1.0] - 2019-12-05

First version of the NESP website

### Added
- flask structure (#1)
- docker deployment files (#12, #26)
- structure of the header (#13)
- structure of the contact section(#14)
- structure of the feature section(#15, #38, #65)
- structure of the about page (#23)
- structure of the maps section (#39)
- script to copy files from NESP2 repository (#39)
- macros to avoid duplicating code (#23, #25)
- text for about-nesp (#24)
- mobile responsiveness of footer (#37)
- structure of the footer license (#48)
- structure of the footer logos (#47)
- structure of the footer contacts (#41)
- hover effects (#51, #52) 
- link with nesp repo (#39)
- page for privacy policy and terms of service (#67)
- cross-linking protection for all external links (#69)
- js folder for javascript code (#71)
- objective page (#132)

### Changed
- structure of the folders --> flask files in `app` folder (#12)
- README with new instruction (#12)

