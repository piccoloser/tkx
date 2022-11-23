# Contribution Guidelines

Thank you for considering contributing to tkx!

These guidelines are to help you make meaningful changes which help improve the project without too much (if any) refactoring on my part. In return for your compliance with this guide, I will reciprocate by addressing your issue, assessing changes, and assisting in the completion of your pull requests!

Of course, when communicating with others and/or contributing, please act in accordance with the [Code of Conduct](./CODE_OF_CONDUCT.md).

## Contributions I'm Looking For

tkx is by no means a massive or hyper complex project, but it's a lot to implement for one developer! There are many ways you can contribute, and many of them don't involve writing *any* code.

### Ideas for Improvement
When creating something that's meant to improve the developer experience, it takes more than *one* developer's opinions and ideas to get a good idea of what changes should be made. By contributing your ideas for features, changes, and improvements, you make the thinking part of all this a lot easier!

### Bug Reports
It would be great if things worked all the time, but that simply isn't the case. To add to that, sometimes a bug might only happen in very specific circumstances that only *you* have encountered. Simply reporting any bugs you encounter along with steps to reproduce said bugs is a huge help in squashing them.

### Bug Fixes and/or Feature Implementations
Code contributions, while subject to review, are highly appreciated! Whether it's fixing a bug, optimizing a feature, or implementing new functionality, any effort that goes towards improving tkx is welcome!

#### Bare-Bones Style Guidelines
* Only import *exactly* what you need (no glob imports).
* General PEP 8 standards apply, but line length is limited to 120 characters instead of 79.
* Code contributions must be formatted with [black](https://pypi.org/project/black/) before a PR is opened.
* Variable names should use snake_case (*All lowercase, separate words with underscores*).
* Class names should use PascalCase (*First letter of every word is capitalized, no spaces*).
* Constant names should use SCREAMING_SNAKE_CASE (*snake_case but caps lock ON*).
  * All constants must be defined in `tkx/constants.py` and imported where needed.

## What I'm Not Looking For
* Please keep the purpose of this project in mind when submitting feature suggestions. tkx is meant to improve the developer's experience when making a GUI application in Python.
  * For example, please do not submit a feature request for an integrated web browser or calculator.

* Please do not use the issue tracker for support requests ("*How do I...?*").

## First Contributions
As of writing, I don't have any Help Wanted or Beginner issues.

If you've never contributed to an open source project before and you would like some resources to get started, check these out:
* https://makeapullrequest.com/
* https://firsttimersonly.com/

