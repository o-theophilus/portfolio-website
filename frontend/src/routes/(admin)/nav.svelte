<script>
	import { page } from '$app/state';
	import { Icon } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';

	let { onclick } = $props();

	const buttons = [
		{
			name: 'Dashboard',
			href: '/admin',
			access: null,
			icon: 'layout-dashboard'
		},
		{
			name: 'Admin',
			href: '/admin/users_admin',
			access: 'user.set_access',
			icon: 'shield-check'
		},
		{
			name: 'Users',
			href: '/admin/users',
			access: 'user.view',
			icon: 'users'
		},
		{
			name: 'Reports',
			href: '/admin/report',
			access: 'report.view',
			icon: 'flag-triangle-right'
		},
		{
			name: 'Blocked Users',
			href: '/admin/block',
			access: 'block.view',
			icon: 'user-x'
		},
		{
			name: 'File Error',
			href: '/admin/file_error',
			access: 'admin.manage_files',
			icon: 'file-warning'
		},
		{
			name: 'Maintenance',
			href: '/admin/maintenance',
			access: 'admin.maintenance',
			icon: 'wrench'
		}
	];

	const buttons2 = $derived([
		{
			name: 'Log',
			href: '/log',
			access: 'log.view',
			icon: 'clipboard-list',
			icon2: 'arrow-up-right'
		}
	]);
</script>

<div class="container">
	<div class="top">
		{#each buttons as x}
			{@const a = x.href.split('/')}
			{@const b = page.url.pathname.split('/')}
			{@const active = a[a.length - 1] == b[b.length - 1]}

			{#if app.user.access.includes(x.access) || x.access === null}
				<a class:active href={x.href} data-sveltekit-preload-data {onclick}>
					<Icon icon={x.icon}></Icon>
					<div class="name" in:slide={{ delay: 200 }}>
						{x.name}

						{#if x.icon2}
							<Icon icon={x.icon2}></Icon>
						{/if}
					</div>
				</a>
			{/if}
		{/each}
	</div>

	<div class="bottom">
		{#each buttons2 as x}
			{#if app.user.access.includes(x.access) || x.access === null}
				<a href={x.href} data-sveltekit-preload-data>
					<Icon icon={x.icon}></Icon>
					<div class="name" in:slide={{ delay: 200 }}>
						{x.name}

						{#if x.icon2}
							<Icon icon={x.icon2}></Icon>
						{/if}
					</div>
				</a>
			{/if}
		{/each}
	</div>
</div>

<style>
	.container {
		position: relative;
		container-type: inline-size;

		display: flex;
		flex-direction: column;
		justify-content: space-between;
		flex-shrink: 0;

		padding: 8px;
		height: 100%;
		overflow-y: auto;
		background-color: var(--bg);
		border-radius: 8px;

		&::before {
			content: '';
			position-anchor: --active;

			position: absolute;
			top: anchor(top);
			right: anchor(right);
			bottom: anchor(bottom);
			width: 4px;

			background-color: var(--cl1);
			border-radius: var(--toggle-border-radius, 4px);

			transition:
				top 0.2s ease-in-out,
				bottom 0.2s ease-in-out;
		}

		& a {
			display: flex;
			align-items: center;
			justify-content: center;
			gap: 16px;

			height: 40px;
			padding: 0 16px;
			border-radius: 8px;

			color: var(--ft2);
			fill: currentColor;
			text-decoration: none;
			font-size: 0.8rem;

			.name {
				display: none;
				align-items: center;
				justify-content: space-between;

				width: 100%;
				overflow: hidden;

				@container (min-width: 100px) {
					display: flex;
				}
			}

			transition:
				background-color 0.2s ease-in-out,
				color 0.2s ease-in-out,
				font-weight 0.2s ease-in-out,
				gap 0.2s ease-in-out,
				width 0.2s ease-in-out,
				padding 0.2s ease-in-out;

			&.active {
				anchor-name: --active;
				color: var(--ft1);
				background-color: var(--bg2);
				font-weight: 800;
			}

			&:hover {
				background-color: var(--bg1);
			}
		}
	}
</style>
