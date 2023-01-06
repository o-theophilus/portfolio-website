// import adapter from '@sveltejs/adapter-auto';
import vercel from '@sveltejs/adapter-vercel';

const config = {
	kit: {
		// adapter: adapter()
		adapter: vercel({
			edge: false,
			external: [],
			split: false
		  })
	}
};

export default config;
