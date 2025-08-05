<script>
	import { scroll } from '$lib/store_old.js';

	import Icon from '$lib/icon.svelte';
	let percent = 0;
	let scrollTop = 0;
</script>

<svelte:window
	on:scroll={() => {
		scrollTop = window.scrollY;
		let winHeight = window.innerHeight;
		let docHeight = document.body.offsetHeight;

		percent = Math.round((scrollTop / (docHeight - winHeight)) * 100);
	}}
/>

<div
	class="circle"
	class:active={scrollTop > 160}
	role="presentation"
	on:click={() => {
		scroll('#top_nav');
	}}
>
	<div class="sector s1" style:--rot="{percent * 3.6}deg" />
	{#if percent >= 25}
		<div class="sector s2" />
	{/if}
	{#if percent >= 50}
		<div class="sector s3" />
	{/if}
	{#if percent >= 75}
		<div class="sector s4" />
	{:else}
		<div class="sector hide" />
	{/if}
	<div class="center">
		<Icon icon="arrow_upward" />
		<!-- {percent} -->
	</div>
</div>

<style>
	.circle {
		--size: 40px;

		position: fixed;
		bottom: var(--sp3);
		right: var(--sp3);
		z-index: 0;

		display: none;
		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		background-color: var(--bg2);
		opacity: 0;
		overflow: hidden;
		pointer-events: none;

		transition: opacity var(--trans);
	}
	.active {
		opacity: 0.5;
		cursor: pointer;
		pointer-events: all;
	}

	.active:hover {
		opacity: 1;
	}

	.center {
		background-color: var(--bg1);
		z-index: 1;

		font-size: 0.8rem;
		display: flex;
		justify-content: center;
		align-items: center;

		width: calc(var(--size) - (var(--size) / 5));
		height: calc(var(--size) - (var(--size) / 5));
		border-radius: 50%;

		stroke-width: 4px;
	}

	.sector {
		position: absolute;

		width: var(--size);
		height: var(--size);

		background-color: var(--cl1);
	}

	.hide,
	.s1 {
		bottom: 50%;
		right: 50%;
		transform-origin: bottom right;
	}

	.hide {
		background-color: var(--bg2);
	}

	.s1 {
		transform: rotate(calc(var(--rot) / 1));
	}

	.s2 {
		bottom: 50%;
		left: 50%;
		transform-origin: bottom left;
	}
	.s3 {
		top: 50%;
		left: 50%;
		transform-origin: top left;
	}
	.s4 {
		top: 50%;
		right: 50%;
		transform-origin: top right;
	}
</style>
