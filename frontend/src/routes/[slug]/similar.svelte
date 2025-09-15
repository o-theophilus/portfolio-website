<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { app } from '$lib/store.svelte.js';
	import { FoldButton, Link } from '$lib/button';
	import { Spinner, Avatar } from '$lib/macro';

	let { key, refresh } = $props();
	let items = $state([]);
	let open = $state(true);
	let loading = $state(true);

	export const load = async () => {
		loading = true;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/similar/${key}`);
		resp = await resp.json();
		loading = false;

		if (resp.status == 200) {
			items = resp.items;
		}
	};

	const prerender = (post) => {
		app.post = post;
	};
</script>

{#if loading || items.length > 0}
	<div class="title line">
		<div class="page_title line">
			Similar Post{#if items.length > 1}s{/if}
			<Spinner active={loading} size="20" />
		</div>

		{#if !loading}
			<FoldButton
				{open}
				onclick={() => {
					open = !open;
				}}
			/>
		{/if}
	</div>

	{#if open && !loading}
		<div class="area" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each items as item}
				<div class="post">
					<a
						href="/{item.slug}"
						onclick={() => {
							prerender(item);
							refresh(item);
						}}
						onmouseenter={() => prerender(item)}
					>
						<Avatar size="58" photo={item.photo} no_photo="/no_photo.png" name={item.title}
						></Avatar>
					</a>
					<div class="details">
						<a
							class="link"
							href="/{item.slug}"
							onclick={() => {
								prerender(item);
								refresh(item);
							}}
							onmouseenter={() => prerender(item)}
						>
							{item.title}
						</a>

						{#if item.description}
							<br />
							<div class="desc">
								{item.description}
							</div>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	{/if}
{/if}

<style>
	.title {
		justify-content: space-between;
		margin: 48px 0;
	}

	.area {
		display: grid;
		gap: var(--sp3);
		margin: 48px 0;
	}

	.post {
		display: flex;
		gap: var(--sp2);
	}

	.link {
		text-decoration: none;
		color: var(--ft1);
		font-weight: 700;

		transition: color var(--trans);
	}

	.link:hover {
		color: var(--cl1);
	}

	@media screen and (min-width: 600px) {
		.area {
			grid-template-columns: 1fr 1fr;
		}
	}

	.desc {
		font-size: 0.8rem;
	}
</style>
