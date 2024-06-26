<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { state } from '$lib/store.js';

	// import Loading from '$lib/loading.svelte';
	import Fold from '$lib/button/fold.svelte';
	import Link from '$lib/button/link.svelte';

	export let post_key;
	let posts = [];
	let open = true;
	// let loading = true;

	export const reset = () => {
		posts = [];
		// loading = true;
	};

	export const refresh = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/similar/${post_key}`);
		resp = await resp.json();
		if (resp.status == 200) {
			posts = resp.posts;
		}
		// loading = false;
	};

	const click = (post) => {
		let sn = 'post_item';
		let i = $state.findIndex((x) => x.name == sn);
		if (i == -1) {
			$state.push({
				name: sn,
				data: post
			});
		} else {
			$state[i].data = post;
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

		<Fold
			{open}
			on:click={() => {
				open = !open;
			}}
		/>
	</div>

	{#if open}
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each posts as x, i}
				<div class="post">
					<a
						href="/{x.slug}"
						on:click={() => {
							click(x);
						}}
						on:mouseenter={() => {
							click(x);
						}}
					>
						<img src={x.photos[0] || ''} alt={x.title} onerror="this.src='/site/no_photo.png'" />
					</a>
					<div class="details">
						<Link
							href="/{x.slug}"
							on:click={() => {
								click(x);
							}}
							on:mouseenter={() => {
								click(x);
							}}
						>
							{x.title}
						</Link>
						<br />
						{x.description}
					</div>
				</div>
				{#if i != posts.length - 1}
					<hr />
					<br />
				{/if}
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

	.post {
		display: flex;
		gap: var(--sp2);

		margin-bottom: var(--sp3);
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
</style>
