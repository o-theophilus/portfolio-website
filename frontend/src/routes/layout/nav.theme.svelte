<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import { page } from '$app/stores';
	import SVG from '$lib/svg.svelte';

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/theme`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$user = resp.user;
		} else {
			throw new Error('invalid request');
		}
	};

	$: is_home = $page.url.pathname == '/';
</script>

<button
	class:is_home
	on:click={() => {
		submit();
		$user.setting_theme = $user.setting_theme == 'dark' ? 'light' : 'dark';
	}}
	on:keypress
>
	<div class="switch" class:dark={$user.setting_theme == 'dark'}>
		<div class="state">
			<SVG type="light" size="15" />
		</div>
		<div class="state">
			<SVG type="dark" size="12" />
		</div>
	</div>
</button>

<style>
	button,
	.state {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	button {
		--size: 20px;

		position: relative;
		overflow: hidden;

		fill: var(--ac1);
		border-radius: 50%;

		height: var(--size);
		width: var(--size);

		margin: auto;
		background-color: transparent;
		border: none;

		transition-timing-function: ease-in-out;
	}

	.is_home {
		fill: var(--ac5);
	}

	button:hover {
		color: var(--ac5_);
		background-color: var(--cl1);
	}

	.switch {
		position: absolute;
		top: 0;

		transition: top var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.dark {
		top: -100%;
	}

	.state {
		width: var(--size);
		height: var(--size);
	}
</style>
