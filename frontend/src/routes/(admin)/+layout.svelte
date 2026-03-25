<script>
	import { SideMenu } from '$lib/macro';
	import { Nav } from '../_layout/index.js';
	import AdminNav from './nav.svelte';

	let { children } = $props();

	let menu = $state();
</script>

<div class="container">
	<div class="nav">
		<AdminNav onclick={() => menu.onclick()}></AdminNav>
	</div>

	<div class="page">
		<div class="header">
			<Nav />
		</div>
		{@render children()}
	</div>

	<SideMenu bind:this={menu}>
		<AdminNav onclick={() => menu.onclick()}></AdminNav>
	</SideMenu>
</div>

<style>
	.container {
		display: flex;
	}
	.nav {
		display: none;
		position: sticky;
		top: 0;
		flex-shrink: 0;
		height: 100vh;
		border-right: 1px solid var(--ol);

		transition: width 0.2s ease-in-out;

		@media screen and (min-width: 600px) {
			width: 56px;
			display: block;
		}

		@media screen and (min-width: 700px) {
			width: 180px;
		}
	}

	.page {
		width: 100%;
		.header {
			background-color: var(--bg);
		}
	}
</style>
