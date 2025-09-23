<script>
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { goto } from '$app/navigation';
	import { module, app, page_state } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { LinkArrow, RoundButton } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Tag } from '$lib/button';
	import Edit from './edit.svelte';
	import { onMount } from 'svelte';

	let index = $state(0);

	const set = (dir = 0) => {
		index = index + dir;

		if (index > app.highlight.length - 1) {
			index = 0;
		} else if (index < 0) {
			index = app.highlight.length - 1;
		}
	};

	const prerender = (post) => {
		app.post = post;
	};

	const reset_index = () => {
		index = 0;
	};

	onMount(async () => {
		if (!app.highlight) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlights`);
			resp = await resp.json();

			if (resp.status == 200) {
				app.highlight = resp.items;
			}
		}
	});

	let src = $derived(app.highlight?.[index]?.photo || '/no_photo.png');
</script>

{#if app.highlight?.length > 0 || app.user.access.includes('post:edit_highlight')}
	<Content --content-height="100%" --content-padding-top="80px" --content-padding-bottom="56px">
		<div class="line">
			<div class="page_title">
				Some Thing{app.highlight?.length > 1 ? 's' : ''}
				I've Built
			</div>

			{#if app.user.access.includes('post:edit_highlight')}
				<RoundButton icon="square-pen" onclick={() => module.open(Edit, { reset_index })} />
			{/if}
		</div>

		{#if app.highlight?.length > 0}
			<LinkArrow href="/post" --link-font-size="0.8rem">View more</LinkArrow>

			<br />
			<br />

			<dir class="carousel">
				{#key index}
					<img
						in:fade|local={{ delay: 0, duration: 500, easing: cubicInOut }}
						onclick={() => {
							prerender(app.highlight[index]);
							goto(`/${app.highlight[index].slug}`);
						}}
						onmouseenter={() => {
							prerender(app.highlight[index]);
						}}
						role="presentation"
						{src}
						alt={app.highlight[index].title}
						onerror={() => (src = '/no_photo.png')}
					/>
				{/key}
				<div class="hidden">
					{#each Array(app.highlight.length) as _, i}
						<img src={app.highlight[i].photo || '/no_photo.png'} alt={app.highlight[i].title} />
					{/each}
				</div>

				{#if app.highlight.length > 1}
					<div class="nav">
						<button
							onclick={() => {
								set(-1);
							}}
						>
							<Icon icon="chevron-left" />
						</button>

						<button
							onclick={() => {
								set(1);
							}}
						>
							<Icon icon="chevron-right" />
						</button>
					</div>

					<div class="indicator">
						{#each Array(app.highlight.length) as _, i}
							<button
								class="one"
								class:active={i == index}
								onclick={() => {
									index = i;
								}}
							>
								<span style:display="none">hidden</span></button
							>
						{/each}
					</div>
				{/if}
			</dir>

			{#key index}
				<div class="info" in:fade|local={{ delay: 0, duration: 500, easing: cubicInOut }}>
					<a href="/{app.highlight[index].slug}" class="name">
						{app.highlight[index].title}
					</a>

					{#if app.highlight[index].description}
						<div class="description">
							{app.highlight[index].description}
						</div>
					{/if}

					{#if app.highlight[index].tags.length > 0}
						<div class="line tag">
							{#each app.highlight[index].tags as x}
								<Tag onclick={() => page_state.goto('post', { tag: x })}>{x}</Tag>
							{/each}
						</div>
					{/if}
				</div>
			{/key}
		{/if}
	</Content>
{/if}

<style>
	.carousel {
		position: relative;
		aspect-ratio: 4/3;

		display: flex;
		align-items: center;
		justify-content: center;

		border-radius: var(--sp1);
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.449);
		outline: 2px solid transparent;

		overflow: hidden;
		transition: outline-color;
	}
	.carousel:has(img:hover) {
		outline-color: var(--cl1);
	}

	@media screen and (min-width: 700px) {
		.carousel {
			aspect-ratio: 4/2;
		}
	}

	img {
		width: 100%;
		height: 100%;

		object-fit: cover;
		background-color: var(--bg2);
		cursor: pointer;
	}

	.hidden {
		width: 0;
		height: 0;
	}

	.nav {
		position: absolute;
		bottom: 0;
		left: 0;

		display: flex;
		padding: 6px;
		gap: 4px;
		pointer-events: none;
	}

	.nav button {
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		border: none;
		width: 40px;
		height: 40px;
		border-radius: var(--sp0);

		background-color: black;
		color: white;
		cursor: pointer;
		pointer-events: all;

		transition: background-color var(--trans);
	}
	.nav button:hover {
		background-color: var(--cl1);
	}

	.indicator {
		--size: 12px;
		--gap: 6px;

		position: absolute;
		bottom: 0;
		right: 0;

		display: flex;
		gap: var(--gap);
		justify-content: center;

		background-color: black;
		padding: var(--gap);
		margin: var(--sp1);
		border-radius: calc((var(--size) + var(--size) * 2) / 2);
	}

	.indicator button {
		flex-shrink: 0;
		width: var(--size);
		height: var(--size);

		background-color: gray;
		border-radius: calc(var(--size) / 2);
		border: none;
		cursor: pointer;

		transition:
			width var(--trans),
			background-color var(--trans);
	}

	.indicator button.active {
		width: calc(var(--size) * 2);
		background-color: white;
	}
	.indicator button:hover {
		background-color: var(--cl1);
	}

	.info {
		max-width: 400px;
	}
	.name {
		display: inline-block;

		color: var(--ft1);
		font-weight: 700;
		font-size: 1.2rem;
		text-decoration: none;

		transition: color var(--trans);
	}
	.name:hover {
		color: var(--cl1);
	}

	.name,
	.description {
		margin-top: var(--sp2);
	}

	.tag {
		margin-top: 16px;
		gap: 4px;
	}
</style>
