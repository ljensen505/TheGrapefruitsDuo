# The Grapefruits Duo

Frontend client for Eugene, OR based chamber music duo, The Grapefruits Duo. Publicly available at [thegrapefruitsduo.com](https://thegrapefruitsduo.com/). This client consumes a RESTful API built with FastAPI and publicly available at [api.thegrapefruitsduo.com](https://api.thegrapefruitsduo.com/). Back-end source code available on [GitHub](https://github.com/ljensen505/thegrapefruitsduo-back).

## Features

The customer-facing page for this SPA is relatively simple. It includes sections for the group itself, each memeber, upcoming events, and a contact form. The admin portal is where the real magic happens. Once authenticated, the user (a member of the group, or myself) can utlilze full CRUD operations on most entities including events, bios, and headshots.

### Getting started

```bash
git clone https://github.com/ljensen505/thegrapefruitsduo-front
```

```bash
cd thegrapefruitsduo-front
```

```bash
npm install
npm run dev
```

### Technologies Used

- React
- TypeScript
- Bootstrap 5
- Axios
- oauth2
- Font Awesome
- Cloudinary

Initialized with Vite.

### Deployment Info

- Hosted on a Linode server running Ubuntu 22.04
- Reverse proxy managed with Nginx on port 6001
- SSL certificate provided by Let's Encrypt
- Managed with systemd
- DNS managed with Google Domains (for now...)

### Development Notes

When running locally, it is expected that the API is running on localhost:8000. This can be changed in the `.env` file (this file may need to be created). See `.env.example` for an example and more info.
