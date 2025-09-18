<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { page } from '$app/state';

	import { app } from '$lib/store.svelte.js';
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	import { onMount } from 'svelte';

	let nots = $state([]);

	const format = (x) => {
		if (x.type == 'unused_files') {
			x.type = `${x.count} unused file${x.count > 1 ? 's' : ''}`;
		}
		return x;
	};

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/notification`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();

		if (resp.status == 200) {
			nots = resp.nots.map((x) => format(x));
		}
	});

	let open = $state(false);
	let self = $state(false);
</script>

<svelte:window
	onclick={() => {
		if (open && !self) {
			open = false;
		}
		self = false;
	}}
/>

{#if nots.length}
	<div class="comp">
		<button
			class:is_home={page.url.pathname == '/'}
			onclick={() => {
				open = !open;
				self = true;
			}}
		>
			<div class="new"></div>
			<Icon icon="bell"></Icon>
		</button>

		{#if open}
			<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
				<div class="title">
					Notification{#if nots.length > 1}s{/if}
				</div>
				{#each nots as x}
					<a href={x.slug}>
						{x.type}
					</a>
				{/each}
			</div>
		{/if}
	</div>
{/if}

<style>
	.comp {
		position: relative;
	}

	button {
		--size: 20px;

		display: flex;
		justify-content: center;
		align-items: center;
		position: relative;

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

	.new {
		--size: 8px;

		flex-shrink: 0;
		position: absolute;
		top: 0px;
		right: 0px;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;
		background-color: red;
	}

	.menu {
		position: absolute;
		top: 40px;
		left: -90px;
		z-index: 1;

		display: flex;
		flex-direction: column;

		width: 200px;
		background-color: var(--bg1);
		border-radius: var(--sp0);

		outline: 2px solid var(--bg2);
	}

	.title {
		padding: 4px 16px;
		font-size: 0.7rem;
		font-weight: 800;
	}

	a {
		padding: 8px 16px;
		text-decoration: none;
		color: var(--ft1);

		transition: background-color var(--trans);
	}
	a:hover {
		background-color: var(--bg2);
	}
	.title,
	a:not(:last-child) {
		border-bottom: 2px solid var(--bg2);
	}
</style>
