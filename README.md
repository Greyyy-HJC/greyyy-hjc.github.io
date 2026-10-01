
<h1 align="center">
AcadHomepage
</h1>

<div align="center">

[![](https://img.shields.io/github/stars/RayeRen/acad-homepage.github.io)](https://github.com/RayeRen/acad-homepage.github.io)
[![](https://img.shields.io/github/forks/RayeRen/acad-homepage.github.io)](https://github.com/RayeRen/acad-homepage.github.io)
[![](https://img.shields.io/github/issues/RayeRen/acad-homepage.github.io)](https://github.com/RayeRen/acad-homepage.github.io)
[![](https://img.shields.io/github/license/RayeRen/acad-homepage.github.io)](https://github.com/RayeRen/acad-homepage.github.io/blob/main/LICENSE)  | [中文文档](./docs/README-zh.md) 
</div>

<p align="center">A Modern and Responsive Academic Personal Homepage</p>

<p align="center">
    <br>
    <img src="docs/screenshot.png" width="100%"/>
    <br>
</p>

Some examples:
- [Demo Page](https://rayeren.github.io/acad-homepage.github.io/)
- [Personal Homepage of the author](https://rayeren.github.io/)

## Key Features
- **Automatically update INSPIRE-HEP publications and citations**: the official API supplies the complete bibliography for Jinchen.He.1. A daily GitHub Action publishes the refreshed feed; the website retains a local snapshot as fallback.
- **Support Google analytics**: you can trace the traffics of your homepage by easy configuration.
- **Responsive**: this homepage automatically adjust for different screen sizes and viewports.
- **Beautiful and Simple Design**: this homepage is beautiful and simple, which is very suitable for academic personal homepage.
- **SEO**: search Engine Optimization (SEO) helps search engines find the information you publish on your homepage easily, then rank it against similar websites.

## Quick Start

1. Fork this REPO and rename to `USERNAME.github.io`, where `USERNAME` is your github USERNAME.
1. Configure the INSPIRE bibliography using `_data/inspire_config.json` (author record `1935435`). No Google Scholar ID or API key is required. Enable GitHub Actions for the **Update INSPIRE Publications** workflow. It runs daily at 08:00 UTC and can also be started manually. The workflow writes its results to the `inspire-stats` branch; it does not overwrite the website source branch.
1. Generate an initial or updated local snapshot with `python3 inspire_crawler/main.py`. Add personal Poster, Slides, and code links to `_data/publication_extras.json`, keyed by INSPIRE literature record ID. See [INSPIRE maintenance](docs/INSPIRE.md).
1. Generate favicon using [favicon-generator](https://redketchup.io/favicon-generator) and download all generated files to `REPO/images`.
1. Modify the configuration of your homepage `_config.yml`:
    1. `title`: the title of your homepage
    1. `description`: the description of your homepage
    1. `repository`: USER_NAME/REPO_NAME  
    1. `google_analytics_id` (optional): google analytics ID
    1. SEO Related keys (optional): get these keys from search engine consoles (e.g. Google, Bing and Baidu) and paste here.
    1. `author`: the author information of this homepage, including some other websites, emails, city and univeristy.
    1. More configuration details are described in the comments.
1. Add your homepage content in `_pages/main.md`. The publication section is rendered from INSPIRE data.
    1. Other sections can use HTML and Markdown as before. Do not hand-edit generated publication metadata; maintain additional material links separately in `_data/publication_extras.json`.
1. Your page will be published at `https://USERNAME.github.io`.

## Debug Locally

This repository uses Ruby 3.3 for local builds. On macOS, install dependencies with:

```sh
brew install ruby@3.3
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
BUNDLE_PATH="$PWD/vendor/bundle" bundle install
bash run_build.sh
```

`run_build.sh` and `run_server.sh` select Homebrew Ruby 3.3 when available and
use the project-local `vendor/bundle` directory. They do not modify your shell
configuration. On other platforms, provide Ruby 3.3 through your usual runtime
manager. Generated files and installed gems are excluded from Git and the site.

1. Clone your REPO to local using `git clone`.
1. Install Jekyll building environment, including `Ruby`, `RubyGems`, `GCC` and `Make` following [the installation guide](https://jekyllrb.com/docs/installation/#requirements).
1. Run `bash run_server.sh` to start Jekyll livereload server.
1. Open http://127.0.0.1:4000 in your browser.
1. If you change the source code of the website, the livereload server will automatically refresh.
1. When you finish the modification of your homepage, `commit` your changings and `push` to your remote REPO using `git` command.

# Acknowledges

- AcadHomepage incorporates Font Awesome, which is distributed under the terms of the SIL OFL 1.1 and MIT License.
- AcadHomepage is influenced by the github repo [mmistakes/minimal-mistakes](https://github.com/mmistakes/minimal-mistakes), which is distributed under the MIT License.
- AcadHomepage is influenced by the github repo [academicpages/academicpages.github.io](https://github.com/academicpages/academicpages.github.io), which is distributed under the MIT License.
