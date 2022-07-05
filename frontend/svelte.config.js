import vercel from '@sveltejs/adapter-vercel';

const config = {
	kit: {
		adapter: vercel()
	}
};

export default config;
