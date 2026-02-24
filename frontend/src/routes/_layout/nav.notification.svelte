<script>
	import { Icon } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

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
		console.log(resp);

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
			onclick={() => {
				open = !open;
				self = true;
			}}
		>
			<Icon icon="bell"></Icon>
		</button>

		{#if open}
			<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
				<div class="title">
					Notification{#if nots.length > 1}s{/if}
				</div>
				{#each nots as x}
					<a href={x.slug}>
						{x.count}
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
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out;

		&:hover {
			color: white;
			background-color: var(--cl1);
		}

		&::before {
			content: '';
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
	}

	.menu {
		position: absolute;
		top: 40px;
		left: -90px;
		z-index: 1;

		display: flex;
		flex-direction: column;

		width: 200px;
		background-color: var(--bg);
		border-radius: 4px;

		outline: 2px solid var(--bg1);
	}

	.title {
		padding: 4px 16px;
		font-size: 0.7rem;
		font-weight: 800;
	}
	
	a {
		border-top: 1px solid var(--bg1);
		padding: 8px 16px;
		text-decoration: none;
		color: var(--ft1);
		font-size: 0.8rem;

		transition: background-color 0.2s ease-in-out;

		&:hover {
			background-color: var(--bg2);
		}
	}
</style>
