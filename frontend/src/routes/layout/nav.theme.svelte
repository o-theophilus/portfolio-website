<script>
	import { page } from '$app/stores';
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Icon from '$lib/icon.svelte';

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
			$user.setting_theme = resp.user.setting_theme;
		} else {
			throw new Error('invalid request');
		}
	};

	$: is_home = $page.url.pathname == '/';
</script>

{#if $user}
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
				<Icon icon="light_mode" size="16" />
			</div>
			<div class="state">
				<Icon icon="dark_mode" size="16" />
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

		color: var(--ac1);
		border-radius: 50%;

		height: var(--size);
		width: var(--size);

		margin: auto;
		background-color: transparent;
		border: none;
		cursor: pointer;

		transition: color var(--trans), background-color var(--trans);
	}

	.is_home {
		color: var(--ac5);
	}

	button:hover {
		color: var(--ac5_);
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
