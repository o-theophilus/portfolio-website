<script>
	import { onMount } from 'svelte';

	import { page } from '$app/state';
	import { app } from '$lib/store.svelte.js';

	import { Avatar, Icon } from '$lib/macro';
	import { Hamburger } from '$lib/button';
	import Menu from './nav.user.menu.svelte';

	let open = $state(false);
	let self = false;
	let admin = $state(false);
	let { is_home } = $props();

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/access`);
		resp = await resp.json();
		if (resp.status == 200) {
			admin = app.user.access.some((x) => resp.access.includes(x));
		}
	});

	let name = $derived.by(() => {
		const [fn, ln] = app.user.name.split(' ');
		let temp = fn;

		const maxLength = ln ? 17 : 20;
		if (temp.length > maxLength) temp = `${temp.slice(0, maxLength - 1)}.`;
		if (ln) temp += ` ${ln[0]}.`;

		return temp;
	});
</script>

<svelte:window
	onclick={() => {
		if (open && !self) {
			open = false;
		}
		self = false;
	}}
/>

{#snippet _user(details = true)}
	<div class="user_details">
		<Avatar name={app.user.name} photo={app.user.photo} size="32" --avatar-border-radius="50%" />
		{#if details}
			<div class="details">
				<div class="name">
					{name}
				</div>
				<div class="email">
					{app.user.email}
				</div>
			</div>
		{/if}
	</div>
{/snippet}

<div class="user">
	<a href="/@{app.user.username}" class="menu_btn full" class:is_home>
		{@render _user()}
	</a>

	<div class="hamburger">
		<Hamburger
			--hamburger-background-color="transpatent"
			--hamburger-background-color-hover={is_home
				? 'color-mix(in srgb, var(--bg1), transparent 80%)'
				: 'var(--bg2)'}
			--hamburger-color={is_home ? 'var(--bg1)' : 'var(--ft2)'}
			--hamburger-color-hover={is_home ? 'var(--bg1)' : 'var(--ft1)'}
			{open}
			onclick={() => {
				open = !open;
				self = true;
			}}
		></Hamburger>
	</div>

	<button
		class="menu_btn avatar"
		class:is_home
		onclick={() => {
			open = !open;
			self = true;
		}}
	>
		{@render _user(false)}
	</button>

	<Menu {open} {admin}>
		{@render _user()}
	</Menu>
</div>

<style>
	.user {
		position: relative;
		display: flex;
	}

	.menu_btn {
		border: none;
		border-radius: 4px;
		color: var(--ft2);
		background-color: transparent;
		text-decoration: none;
		cursor: pointer;

		transition: background-color var(--trans);
	}
	.menu_btn:hover {
		color: var(--ft1);
		background-color: var(--bg2);
	}
	.menu_btn.is_home {
		color: var(--bg1);
	}
	.menu_btn.is_home:hover {
		background-color: color-mix(in srgb, var(--bg1), transparent 80%);
	}

	.menu_btn.full {
		padding: 4px;
		padding-right: 8px;
	}

	.menu_btn.avatar {
		padding: 4px;
	}

	.hamburger,
	.full {
		display: none;
	}

	@media screen and (min-width: 600px) {
		.hamburger,
		.full {
			display: block;
		}
		.avatar {
			display: none;
		}
	}

	.user_details {
		display: flex;
		align-items: center;
		gap: 8px;
		text-align: left;

		transition: color var(--trans);
	}
	.details {
		display: flex;
		flex-direction: column;
	}
	.name {
		font-size: 0.8rem;
		font-weight: 600;
		line-height: 120%;
	}
	.email {
		font-size: 0.7rem;
		line-height: 120%;

		max-width: 150px;
		overflow: hidden;
		text-overflow: ellipsis;
	}
</style>
