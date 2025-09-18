<script>
	import { page } from '$app/state';
	import { app } from '$lib/store.svelte.js';
	import { Icon } from '$lib/macro';

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/theme`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();

		if (resp.status == 200) {
			app.user = resp.user;
		} else {
			throw new Error('invalid request');
		}
	};
</script>

{#if app.user}
	<button
		class:is_home={page.url.pathname == '/'}
		onclick={() => {
			submit();
			app.user.theme = app.user.theme == 'dark' ? 'light' : 'dark';
		}}
	>
		<div class="switch" class:dark={app.user.theme == 'dark'}>
			<div class="state">
				<Icon icon="sun" />
			</div>
			<div class="state">
				<Icon icon="moon" />
			</div>
		</div>
	</button>
{/if}

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

		color: var(--ft2);
		border-radius: 50%;

		height: var(--size);
		width: var(--size);

		background-color: transparent;
		border: none;
		cursor: pointer;

		transition:
			color var(--trans),
			background-color var(--trans);
	}

	.is_home {
		color: var(--bg1);
	}

	button:hover {
		color: white;
		background-color: var(--cl1);
	}

	.switch {
		position: absolute;
		top: 0;
		transition: top var(--trans);
	}
	.dark {
		top: -100%;
	}

	.state {
		width: var(--size);
		height: var(--size);
	}
</style>
