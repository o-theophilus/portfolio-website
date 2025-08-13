<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { app } from '$lib/store.svelte.js';
	import { FoldButton, Link } from '$lib/button';
	import { Spinner } from '$lib/macro';

	let { post_key } = $props();
	let posts = $state([]);
	let open = $state(true);
	let loading = $state(true);

	export const load = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/similar/${post_key}`);
		resp = await resp.json();
		loading = false;

		if (resp.status == 200) {
			posts = resp.posts;
		}
	};

	const prerender = (post) => {
		app.post = post;
	};
</script>

{#if loading || posts.length > 0}
	<hr />
	<div class="title line">
		<strong class="ititle line">
			Similar Post{#if posts.length > 1}s{/if}
			<Spinner active={loading} size="20" />
		</strong>

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
			{#each posts as x}
				<div class="post">
					<a href="/{x.slug}" onclick={() => prerender(x)} onmouseenter={() => prerender(x)}>
						<img src={x.photo || '/no_photo.png'} alt={x.title} />
					</a>
					<div class="details">
						<a
							class="link"
							href="/{x.slug}"
							onclick={() => prerender(x)}
							onmouseenter={() => prerender(x)}
						>
							{x.title}
						</a>

						{#if x.description}
							<br />
							<div class="desc">
								{x.description}
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
		margin: var(--sp2) 0;
	}

	.area {
		display: grid;
		gap: var(--sp3);
		margin: var(--sp2) 0;
	}

	.post {
		display: flex;
		gap: var(--sp2);

		/* margin-bottom: var(--sp3); */
	}

	img {
		display: block;

		height: 58px;
		aspect-ratio: 1 / 1;

		object-fit: cover;
		background-color: var(--bg2);
		border-radius: var(--sp1);

		flex-shrink: 0;
		flex-grow: 0;
	}

	.link {
		/* text-decoration: none; */
		color: var(--ft1);
		/* font-weight: 700;

		transition: color var(--trans); */
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
