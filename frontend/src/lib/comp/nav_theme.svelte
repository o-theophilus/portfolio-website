<script>
	import { api_url, _user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import { page } from '$app/stores';
	import SVG from '$lib/comp/svg.svelte';

	const submit = async () => {
		const resp = await fetch(`${api_url}/user/theme`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				$_user = data.data.user;
			} else {
				throw new Error('invalid request');
			}
		}
	};

	$: is_home = $page.url.pathname == '/';
</script>

<button
	class:is_home
	on:click={() => {
		submit();
		$_user.setting.theme = $_user.setting.theme == 'dark' ? 'light' : 'dark';
	}}
	on:keypress
>
	<div class="switch" class:dark={$_user.setting.theme == 'dark'}>
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

		fill: var(--accent1);
		border-radius: 50%;

		height: var(--size);
		width: var(--size);

		margin: auto;
		background-color: transparent;
		border: none;

		transition-timing-function: ease-in-out;
	}

	.is_home {
		fill: var(--accent5);
	}

	button:hover {
		color: var(--accent5_);
		background-color: var(--color1);
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
