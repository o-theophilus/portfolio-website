import { browser } from '$app/environment';
import { goto, invalidate } from '$app/navigation';
import { page } from '$app/state';

export const app = $state({
	user: {},
	login: false,
	highlight: null,
	tags: null,
	post: {},

	token_name: 'token',
	get token() {
		let cookies = document.cookie.split(';');
		for (let i in cookies) {
			let temp = cookies[i].split('=');
			if (temp[0].trim() === this.token_name) {
				return temp[1];
			}
		}
		return '';
	},
	set token(v) {
		let day = v ? 1 : -10000;
		let date = new Date();
		date.setTime(date.getTime() + day * 24 * 60 * 60 * 1000);
		if (browser) {
			document.cookie = `${this.token_name}=${v};expires=${date.toUTCString()};path=/`;
		}
	}
});


export let module = $state({
	module: null,
	value: {},
	open(module, value = {}) {
		this.module = module
		this.value = value
	},
	close() {
		this.module = null;
		this.value = {};
	}
});

export let loading = $state({
	value: null,
	open(message = 'Loading . . .') {
		this.value = message
	},
	close() {
		this.value = null;
	}
});

export let notify = $state({
	value: [],
	open(message, status = 200) {
		this.value.push({
			message,
			status,
			key: () => {
				const chars = '0123456789abcdef';
				let code = '#';

				for (let i = 0; i < 10; i++) {
					code += chars[Math.floor(Math.random() * chars.length)];
				}
				return code;
			}
		});
	},
	close(key) {
		this.value = this.value.filter((x) => x.key != key);
	}
});




export const page_state = $state({
	state: {},
	refresh() {
		this.state[page.data.page_name].loaded = false
		let ss = new URLSearchParams(this.state[page.data.page_name].searchParams);
		page.url.search = ss.toString()
		loading.open()
		goto(page.url.href, { replaceState: true, invalidate: [true] });
		window.scrollTo({ top: 0, behavior: 'smooth' });
	},
	clear(page_name) {
		this.state[page_name] = {
			searchParams: {},
			data: [],
			loaded: false
		}
	},
	goto(page_name, obj) {
		this.clear(page_name);
		this.state[page_name].searchParams = obj;
		goto(`/${page_name}`);
	},
	set(obj) {
		for (const [key, val] of Object.entries(obj)) {
			this.state[page.data.page_name].searchParams[key] = val
			if (!val) delete this.state[page.data.page_name].searchParams[key]
			if (key != "page_no") delete this.state[page.data.page_name].searchParams["page_no"]
		}
		this.refresh();
	},
	get searchParams() { return this.state[page.data.page_name].searchParams }
})



export let isMobile = $state(false)
export const scroll = (query) => {
	let e = document.querySelector(query);

	const scrollMobile = () => {
		e.scrollIntoView({ behavior: 'smooth' });
	};

	const scrollDesktop = () => {
		const offset = 70;
		const bodyRect = document.body.getBoundingClientRect().top;
		const elementRect = e.getBoundingClientRect().top;
		const elementPosition = elementRect - bodyRect;
		const offsetPosition = elementPosition - offset;

		window.scrollTo({
			top: offsetPosition,
			behavior: 'smooth'
		});
	};

	isMobile ? scrollMobile() : scrollDesktop();
};
