# Candlestick Web App (2.0)
This is the web app for the RGB Candlestick.

It's a `React` application written in `TypeScript`, created with `Vite` and `NodeJS`.

WARNING: I'm absolutely not a frontend developer. 90% of the code here is AI generated and I really don't know what I'm doing!

## Preview

<img src="./preview.png" width="500">

## Development environment

First you must have a working installation of Node.JS. Install it in your preferred way:
[https://nodejs.org/](https://nodejs.org/)

### Install dependencies

With Node.JS installed, the build dependencies can be installed by:
```bash
npm install
```

### Run dev server

Now a development server can be started with:

```bash
npm run dev
```
Which gives a local web server at `http://localhost:5173` where changes could be viewed live.

### Compile

To compile the code and create a production site, run:
```bash
npm run build
```
This will generate an `index.html` + the javascript files in `./assets`. These files could then be served by any web server.


### Cleanup / troubleshooting

If moving the development environment between computers, or if the node modules gets messed up it can be cleaned by:
```bash
rm -rf node_modules package-lock.json
```

