# [The Grapefruits Duo](https://thegrapefruitsduo.com/)

This repo is for Eugene based chamber duo, The Grapefruits Duo. It roughly follows MVC architecture, with structured data persisted with MariaDB, server-side logic with FastAPI, and client-side logic with React & TypeScript.

## Info and Instructions

More info on each part of the project can be found in their respective directories, along with setup instructions. The application is served from a Linode Ubuntu 22.04 instance running NGINX and SSL certificates from Let's Encrypt.

- [Client](https://github.com/ljensen505/TheGrapefruitsDuo/tree/main/client)
- [Server](https://github.com/ljensen505/TheGrapefruitsDuo/tree/main/server)

## Auth

There is no mechanism for creating a user account. Current users have been manually added to the database based on being a member of the ensemble or a site administrator. Authentication is done with Google OAuth2 and is accessed via the Admin dropdown in the navbar.

### Edit Mode

Edit Mode is only available authenticated users.

Logged out:
![Group Bio Logged out](https://res.cloudinary.com/dreftv0ue/image/upload/v1716766796/Screenshot_from_2024-05-26_16-37-60_hethrg.png "Logged out")

Logged in:
![Group Bio Logged In](https://res.cloudinary.com/dreftv0ue/image/upload/v1716766768/Screenshot_from_2024-05-26_16-37-17_rxsd84.png "Logged in")
![Group Bio Edit Form](https://res.cloudinary.com/dreftv0ue/image/upload/v1716767454/Screenshot_from_2024-05-26_16-50-41_rahdzn.png "Edit Form")

Similar buttons and forms exist for editing indivdual musician bios, headshots, and upcoming events.

![Event Addition Form](https://res.cloudinary.com/dreftv0ue/image/upload/v1716767722/Screenshot_from_2024-05-26_16-54-45_ow0kne.png "Event Addition Form")
