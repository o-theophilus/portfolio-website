<script>
	import { Button } from '$lib/button';
	import { slide } from 'svelte/transition';

	let { children } = $props();

	let open = $state(false);
	let menu = $state();
	let can_close = $state(false);

	export const onclick = () => {
		open = false;
		can_close = false;
	};
</script>

<svelte:window
	onresize={(e) => {
		if (e.target.innerWidth > 600) {
			open = false;
		}
	}}
	onclick={(e) => {
		if (menu && menu.contains(e.target)) return;
		if (open && !can_close) open = false;
		can_close = false;
	}}
/>

<div class="menu_open">
	<Button
		icon="panel-left-open"
		onclick={() => {
			open = !open;
			can_close = true;
		}}
	></Button>
</div>

{#if open}
	<div transition:slide class="menu" bind:this={menu} class:open>
		{@render children()}
	</div>
{/if}

<style>
	.menu {
		position: fixed;
		bottom: var(--side_menu-bottom, 0);
		overflow-y: auto;
		left: 0;
		right: 0;
		z-index: 1;

		height: 300px;
		transition: bottom 0.2s ease-in-out;
	}

	.menu_open {
		padding: 16px;
		position: fixed;
		bottom: var(--side_menu-bottom, 0);
		left: 0;
		z-index: 1;
		--button-width: 40px;
		--button-height: 40px;
	}

	@media screen and (min-width: 600px) {
		.menu_open,
		.menu {
			display: none;
		}
	}
</style>
