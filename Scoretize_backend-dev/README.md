
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/logo.png" alt="Logo" height="80">
  </a>
<h3 align="center">Scoretize Backend</h3>

  <p align="center">
    <br />
    <a href="https://github.com/TheKeenfolksDigital/Scoretize_backend"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/TheKeenfolksDigital/Scoretize_backend/issues">Report Bug</a>
    ·
    <a href="https://github.com/TheKeenfolksDigital/Scoretize_backend/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#endpoints">Endpoints</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Scoretize is a SaaS platform that allows you to measure and manage a brand digital performance compared with that of competitors.


### Built With

[![Python][python.py]][python-url]
[![Django][django.py]][django-url]
[![DjangoR][djangor.py]][djangor-url]
[![Azure][azure-sql]][azure-url]
<!-- GETTING STARTED -->
## Getting Started

This application is an API connected to a SQLServer database.

### Prerequisites

Python > 3.8 
  ```sh
  https://www.python.org/downloads/
  ```
PIP installed 
  ```sh
  https://pypi.org/
  ```
Azure DB **firewall enabled** for current IP address.
  
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/TheKeenfolksDigital/Scoretize_backend
   ```
2. Change to app directory
   ```sh
   cd scoretize_backend
   ```
3. Create a virtual environment
   ```sh
   python3 -m venv env
   ```
3. Go inside virtual environment
   ```sh
   source env/bin/activate
   ```
4. Install al requirements
   ```sh
   pip install -r requirements.txt
   ```
5. Run the project
   ```sh
   bash run.sh
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Endpoints

### Global
<p>global/global/global-score/'id'</p>
<p>global/global/global-score/'id'/direct-competitors</p>

### Overview
  <p>overview/overview/website-score/'id'/evolution/</p>
  <p>overview/overview/seo-score/'id'/evolution/</p>
  <p>overview/overview/paid-media/'id'/evolution/</p>
  <p>overview/overview/socialMedia-score/'id'/evolution/</p>
  
### Website 
<p>website/website/website-score/{{ _.id }}/</p>
<p>website/website/website-score/{{ _.id }}/evolution/</p>
<p>website/website/website-score/{{ _.id }}/traffic-country/</p>
<p>website/website/website-score/{{ _.id }}/direct-competitors/</p>
<p>website/website/website-score/{{ _.id }}/traffic-sources/graph/</p>
<p>website/website/website-score/{{ _.id }}/social-sources/</p>
<p>website/website/website-score/{{ _.id }}/traffic-sources/competitors/</p>

### Seo
<p>seo/seo/seo-score/{{ _.id }}/</p>
<p>seo/seo/seo-score/{{ _.id }}/evolution</p>
<p>seo/seo/seo-score/{{ _.id }}/traffic-evolution</p>
<p>seo/seo/seo-score/{{ _.id }}/keywords-graph/</p>
<p>seo/seo/seo-score/{{ _.id }}/direct-competitors/</p>

### Paid Media
<p>paid-media/paid-media/paid-media/{{ _.id }}/</p>
<p>paid-media/paid-media/paid-media/{{ _.id }}/direct-competitors</p>

### Social Media
<p>socialMedia/socialMedia/socialMedia-score/{{ _.id }}/</p>
<p>socialMedia/socialMedia/socialMedia-score/{{ _.id }}/direct-competitors</p>

### Facebook
<p>socialMedia/socialMedia/facebook-score/{{ _.id }}/</p>
<p>socialMedia/socialMedia/facebook-score/{{ _.id }}/direct-competitors</p>

### Instagram
<p>socialMedia/socialMedia/instagram-score/{{ _.id }}/</p>
<p>socialMedia/socialMedia/instagram-score/{{ _.id }}/direct-competitors</p>

### Twitter
<p>socialMedia/socialMedia/twitter-score/{{ _.id }}/</p>
<p>socialMedia/socialMedia/twitter-score/{{ _.id }}/direct-competitors</p>

### Youtube
<p>socialMedia/socialMedia/youtube-score/{{ _.id }}/</p>
<p>socialMedia/socialMedia/youtube-score/{{ _.id }}/direct-competitors</p>

### User Register
<p>user/register/create-profile/</p>
<p>user/register/active-profile/</p>

### User Login
<p>user/user/login/</p>

### Project
<p>project/project/create-project/</p>
<p>project/project/get-projects/</p>
<p>project/project/get-project/{{ _.id }}</p>
<p>project/project/delete-project/{{ _.id }}</p>
<p>project/project/active-project/{{ _.id }}</p>
<p>project/project/failed-project/{{ _.id }}</p>

### ChronTrigger
<p>chron/chron/company-scrapping/</p>
<p>chron/chron/update-project/{{ _.id }}</p>
<p>chron/chron/update-engagement-rate/</p>

### Settings
<p>settings/sector/postSectors/</p>
<p>settings/sector/sectors/</p>
<p>settings/user_type/user-type/</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p> 


<!-- ROADMAP
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>  -->



<!-- CONTRIBUTING 
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- LICENSE 
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- CONTACT 
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- ACKNOWLEDGMENTS 
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt

[azure-sql]: https://img.shields.io/badge/Microsoft%20SQL%20Sever-CC2927?style=for-the-badge&logo=microsoft%20sql%20server&logoColor=white
[azure-url]: https://azure.microsoft.com/

[product-screenshot]: images/screenshot.png

[python.py]: https://camo.githubusercontent.com/a1b2dac5667822ee0d98ae6d799da61987fd1658dfeb4d2ca6e3c99b1535ebd8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d3336373041303f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d666664643534
[python-url]: https://www.python.org/
[django.py]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[django-url]: https://www.djangoproject.com/
[djangor.py]: https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray
[djangor-url]: https://www.django-rest-framework.org/
