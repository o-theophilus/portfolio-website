<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { memory } from '$lib/store.svelte.js';

	import { FoldButton, Link } from '$lib/button';

	let { post_key } = $props();
	let posts = $state([]);
	let open = $state(true);

	export const reset = () => {
		posts = [];
	};

	export const refresh = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/similar/${post_key}`);
		resp = await resp.json();
		if (resp.status == 200) {
			posts = resp.posts;
		}
	};

	const click = (post) => {
		let sn = 'post_item';
		let i = $memory.findIndex((x) => x.name == sn);
		if (i == -1) {
			$memory.push({
				name: sn,
				data: post
			});
		} else {
			$memory[i].data = post;
		}
	};
</script>

{#if posts.length > 0}
	<hr />
	<div class="title line">
		<strong class="ititle line">
			Similar Posts
			<!-- <Loading active={loading} size="20" /> -->
		</strong>

		<FoldButton
			{open}
			onclick={() => {
				open = !open;
			}}
		/>
	</div>

	{#if open}
		<div class="area" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each posts as x, i}
				<div class="post">
					<a href="/{x.slug}" onclick={() => click(x)} onmouseenter={() => click(x)}>
						<img src={x.photo || '/no_photo.png'} alt={x.title} />
					</a>
					<div class="details">
						<!-- <a
							class="link"
							href="/{x.slug}"
							onclick={() => {
								click(x);
							}}
							on:mouseenter={() => {
								click(x);
							}}
						>
							{x.title}
						</a> -->

						<Link
							href="/{x.slug}"
							onclick={() => {
								click(x);
							}}
							on:mouseenter={() => {
								click(x);
							}}
						>
							<span class="link">
								{x.title}
							</span>
						</Link>

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

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
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
