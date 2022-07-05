# Theophilus.website
This website is an all-in-one blog, portfolio and pet project, It was Built from scratch with SvelteKit and deployed on Vercel.
<br>
<br>

# Todo

* Fix
	1. [ ] review form message

* Features
	1. [ ] add blog to home
	1. [ ] dark mode
	1. [ ] site search
	1. [ ] scroll to top
	1. [ ] add database

<br>
<br>


# Deploy on vercel

Add

```
"@sveltejs/adapter-vercel": "next"
```

to the devDependencies in your `package.json` file and run

```
npm install.
```

in `svelte.config.cjs`, set the adapter

```javascript
import vercel from '@sveltejs/adapter-vercel';

module.exports = {
	kit: {
		...
		adapter: vercel()
	}
};
```
