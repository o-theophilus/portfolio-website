<script>
	import { page } from '$app/stores';
	import { openMobileMenu, isMobile } from '$lib/store.js';
	import SVG from '$lib/svg.svelte';

	export let name;
	export let link;

	let page_;
	link = link === undefined ? name : link;
	page_ = link === '' ? undefined : link;
	$: segment = $page.url.pathname.split('/')[1] || undefined;
</script>

<a
	class="link"
	class:active={segment === page_}
	href="/{link}"
	on:click={() => {
		$openMobileMenu = false;
	}}
>
	<div class="block">
		{#if $isMobile}
			<SVG type={name} />
		{/if}
		<div class="text">{name.replace('_', ' ')}</div>
	</div>
</a>

<style>
	.link {
		display: flex;
		justify-content: center;
		align-items: center;

		width: 100%;
		height: var(--headerHeight);

		text-decoration: none;
		color: var(--color1);

		background-color: var(--colorNill);

		text-transform: capitalize;
		fill: var(--color1);

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	/* @media screen and (min-width: 900px) {
		.link {
			height: 100%;
		}
	} */
	.link:hover {
		background-color: var(--color5);
	}

	.active {
		font-weight: bold;
		background-color: var(--color5);

		border-color: var(--color3);
		border-width: 10px;
		border-width: 5px;
		border-bottom-style: solid;

		fill: var(--color3);
	}

	.block {
		display: flex;
		width: 100%;
		padding: 0 20px;
	}
	.text {
		margin: auto;
	}
</style>
