<script>
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import Content from '$lib/content.svelte';
	import ItemBox from './3_post.item_box.svelte';
	import Scroller from '$lib/scroller.svelte';

	let sticky;
	let block;
	let section;
	let scroller = {};
	let pos = {};

	export let posts = [];

	let observe_post = posts.length > 0 ? posts[0] : {};
	let hover_post = {};
	$: active_post = Object.keys(hover_post).length > 0 ? hover_post : observe_post;

	const set_pos = (scroller) =>
		(sticky.offsetTop / (section.clientHeight - sticky.clientHeight)) *
		(scroller.clientWidth - block.clientWidth);

	let intersecting = false;
	onMount(() => {
		if (browser) {
			let ob = new IntersectionObserver(
				(entries) => {
					intersecting = entries[0].isIntersecting;
				},
				{
					threshold: 0.9
				}
			);

			ob.observe(document.querySelector('.post-block'));
		}
	});
</script>

<svelte:window
	on:scroll={(e) => {
		pos.a = set_pos(scroller.a);
	}}
/>

<section bind:this={section} class:intersecting>
	<div class="sticky" bind:this={sticky}>
		<div class="bg-area">
			{#key active_post.key}
				<div
					class="bg"
					style:--fff="url({import.meta.env.VITE_BACKEND}/{active_post.photos[0]})"
					in:fade={{ delay: 0, duration: 1000, easing: cubicInOut }}
				/>
			{/key}
		</div>
		<Content>
			<div class="post-block" bind:this={block}>
				<strong class="big title"> Post{posts.length > 1 ? 's' : ''} </strong>

				<div class="scroller" style:right="{pos.a}px" bind:this={scroller.a}>
					{#each posts as post}
						<ItemBox
							parent={block}
							{post}
							{active_post}
							on:active={() => {
								observe_post = post;
							}}
							on:mouseenter={() => {
								hover_post = post;
							}}
							on:mouseleave={() => {
								hover_post = {};
							}}
						/>
					{/each}
					<Scroller href="/post"
						>view
						<br />
						more</Scroller
					>
				</div>

				<div class="desc">
					{#key hover_post.key || observe_post.key}
						<div in:fade={{ delay: 0, duration: 1000, easing: cubicInOut }}>
							<strong class="big color1">
								{hover_post.title || observe_post.title}
							</strong>
							<br />
							{hover_post.description || observe_post.description}
						</div>
					{/key}
				</div>
			</div>
		</Content>
	</div>
</section>

<style>
	section {
		position: relative;
		height: 300vh;
	}

	.title {
		font-size: 30px;
		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.intersecting .title {
		font-size: 40px;
		color: var(--accent1);
	}

	.sticky {
		position: sticky;

		top: 0;
		overflow: hidden;
	}
	.bg-area {
		opacity: 0;
	}
	.intersecting .bg-area {
		opacity: 0.2;
	}
	.bg {
		position: absolute;
		inset: 0;
		background-image: var(--fff);
		background-repeat: no-repeat;
		background-size: cover;
		background-position: center;
		filter: blur(6px);
	}

	.post-block {
		display: flex;
		flex-direction: column;
		justify-content: center;
		height: 100vh;
	}

	.scroller {
		position: relative;

		display: flex;
		align-items: center;
		gap: var(--gap5);
		width: fit-content;

		/* padding-right: var(--gap5); */
		padding: 0 var(--gap5);
	}

	.title,
	.desc {
		height: 30vh;
		display: flex;
		justify-content: center;
		align-items: center;

		text-align: center;
		position: relative;
	}
</style>
