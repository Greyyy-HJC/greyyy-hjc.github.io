---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /main/
  - /main.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

# 👁️‍🗨️ About Me

Hi, this is Jinchen. I major in theoretical physics, also have interests in philosophy and data science.

"The effort to understand the universe is one of the very few things that lifts human life a little above the level of farce, and gives it some of the grace of tragedy." --- Steven Weinberg

“Behind this mask there is more than just flesh. Beneath this mask there is an idea... and ideas are bulletproof.” --- Alan Moore, V for Vendetta

曲终人不见 江上数青峰。--- 钱起 《省试湘灵鼓瑟》

已识乾坤大，犹怜草木青。长空送鸟印，留幻与人灵。--- 马一浮 《旷怡亭口占》

静心得意。


{% include_relative sub/research.md %}

{% include_relative sub/pub.md %}

{% include_relative sub/talk.md %}

{% include_relative sub/edu.md %}

{% include_relative sub/fancy.md %}
