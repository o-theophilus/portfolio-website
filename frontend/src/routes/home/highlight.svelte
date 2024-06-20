<script>
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module, settings, user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Post from './highlight.post.svelte';
	import Edit from './highlight.mod.svelte';
	import Scroller from '$lib/scroller.svelte';
	import BRround from '$lib/button/round.svelte';

	let sticky;
	let block;
	let section;
	let scroller = {};
	let pos = {};

	let observe_post =
		$settings.highlight && $settings.highlight.length > 0 ? $settings.highlight[0] : {};
	let hover_post = {};
	$: active_post = Object.keys(hover_post).length > 0 ? hover_post : observe_post;

	const set_pos = (scroller) =>
		(sticky.offsetTop / (section.clientHeight - sticky.clientHeight)) *
		(scroller.clientWidth - block.clientWidth);

	let intersecting = false;
	onMount(() => {
		if (browser && $settings.highlight) {
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
	let width;
</script>

<svelte:window
	bind:innerWidth={width}
	on:scroll={(e) => {
		pos.a = set_pos(scroller.a);
	}}
/>

{#if $settings.highlight}
	{#if $settings.highlight.length > 0}
		<br /><br />
	{/if}

	<section
		bind:this={section}
		class:intersecting
		style:height="{(width + 64) * $settings.highlight.length + width}px"
	>
		<div class="sticky" bind:this={sticky}>
			<div class="bg-area">
				{#key active_post.key}
					<div
						class="bg"
						style:--bg_img="url({active_post.photos[0]})"
						in:fade={{ delay: 0, duration: 1000, easing: cubicInOut }}
					/>
				{/key}
			</div>
			<Content>
				<div class="post-block" bind:this={block}>
					<div class="title">
						Post{$settings.highlight.length > 1 ? 's' : ''}
						{#if $user.permissions.includes('post:edit_photos')}
							<BRround
								icon="edit"
								large
								on:click={() => {
									$module = {
										module: Edit
									};
								}}
							/>
						{/if}
					</div>

					<div class="scroller" style:right="{pos.a}px" bind:this={scroller.a}>
						{#each $settings.highlight as post (post.key)}
							<Post
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
							more
						</Scroller>
					</div>

					<div class="desc">
						{#key hover_post.key || observe_post.key}
							<div in:fade={{ delay: 0, duration: 1000, easing: cubicInOut }}>
								<strong class="ititle color">
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
{/if}

<style>
	section {
		position: relative;
	}

	.title {
		display: flex;
		gap: var(--sp2);
		font-size: 30px;
		font-weight: 800;

		transition: font-size var(--trans), color var(--trans);
	}
	.intersecting .title {
		font-size: 40px;
		color: var(--ft1);
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
		background-image: var(--bg_img);
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
		gap: var(--sp4);
		width: fit-content;

		padding: 0 var(--sp4);
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
	.color {
		color: var(--cl1);
	}
</style>
