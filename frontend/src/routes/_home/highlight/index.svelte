<script>
	import { goto } from '$app/navigation';
	import { app, module, page_state } from '$lib/store.svelte.js';
	import { cubicInOut } from 'svelte/easing';
	import { fade } from 'svelte/transition';

	import { Button, LinkArrow, RoundButton, Tag } from '$lib/button';
	import { Content } from '$lib/layout';
	import { onMount } from 'svelte';
	import Edit from './edit.svelte';

	let index = $state(0);

	const set = (dir = 0) => {
		index = index + dir;

		if (index > app.featured.length - 1) {
			index = 0;
		} else if (index < 0) {
			index = app.featured.length - 1;
		}
	};
	const prerender = (post) => {
		app.post = post;
	};

	const reset_index = () => {
		index = 0;
	};

	onMount(async () => {
		if (!app.featured) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/posts/feature`);
			resp = await resp.json();

			if (resp.status == 200) {
				app.featured = resp.posts;
			}
		}
	});

	let src = $derived(app.featured?.[index]?.photo || '/no_photo.png');
</script>

{#if app.featured?.length > 0 || app.user.access.includes('post:edit_featured')}
	<Content --content-height="100%" --content-padding-top="80px" --content-padding-bottom="56px">
		<div class="line">
			<div class="page_title">
				Some Thing{app.featured?.length > 1 ? 's' : ''}
				I've Built
			</div>

			{#if app.user.access.includes('post:edit_featured')}
				<RoundButton icon="square-pen" onclick={() => module.open(Edit, { reset_index })} />
			{/if}
		</div>

		{#if app.featured?.length > 0}
			<LinkArrow href="/post" --link-font-size="0.8rem">View more</LinkArrow>

			<br />
			<br />

			<dir class="carousel">
				{#key index}
					<img
						in:fade|local={{ delay: 0, duration: 500, easing: cubicInOut }}
						onclick={() => {
							prerender(app.featured[index]);
							goto(`/${app.featured[index].slug}`);
						}}
						onmouseenter={() => {
							prerender(app.featured[index]);
						}}
						role="presentation"
						{src}
						alt={app.featured[index].title}
						onerror={() => (src = '/no_photo.png')}
					/>
				{/key}
				<div class="hidden">
					{#each Array(app.featured.length) as _, i}
						<img src={app.featured[i].photo || '/no_photo.png'} alt={app.featured[i].title} />
					{/each}
				</div>

				{#if app.featured.length > 1}
					<div class="nav">
						<Button icon="chevron-left" onclick={() => set(-1)}></Button>
						<Button icon="chevron-right" onclick={() => set(1)}></Button>
					</div>

					<div class="indicator">
						{#each Array(app.featured.length) as _, i}
							<button
								class="one"
								class:active={i == index}
								onclick={() => {
									index = i;
								}}
							>
								<span style:display="none">hidden</span>
							</button>
						{/each}
					</div>
				{/if}
			</dir>

			{#key index}
				<div class="info" in:fade|local={{ delay: 0, duration: 500, easing: cubicInOut }}>
					<a href="/{app.featured[index].slug}" class="name">
						{app.featured[index].title}
					</a>

					{#if app.featured[index].description}
						<div class="description">
							{app.featured[index].description}
						</div>
					{/if}

					{#if app.featured[index].tags.length > 0}
						<div class="line tag">
							{#each app.featured[index].tags as x}
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

		border-radius: 8px;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.449);
		outline: 2px solid transparent;

		overflow: hidden;
		transition: outline-color 0.2s ease-in-out;
	}
	.carousel:has(img:hover) {
		outline-color: var(--ft1);
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
		padding: 8px;
		gap: 4px;
		pointer-events: none;

		--button-width: 40px;
		--button-height: 40px;
	}

	.indicator {
		--size: 8px;
		--gap: 6px;

		position: absolute;
		bottom: 0;
		right: 0;

		display: flex;
		gap: var(--gap);
		justify-content: center;

		background-color: black;
		padding: var(--gap);
		margin: 8px;
		border-radius: calc((var(--size) + var(--size) * 2) / 2);

		& button {
			flex-shrink: 0;
			width: var(--size);
			height: var(--size);

			background-color: hsl(0, 0%, 50%);
			border-radius: calc(var(--size) / 2);
			border: none;
			cursor: pointer;

			transition:
				width 0.2s ease-in-out,
				background-color 0.2s ease-in-out;

			&.active {
				width: calc(var(--size) * 3);
				background-color: white;
			}
			&:hover {
				background-color: hsl(0, 0%, 70%);
			}
		}
	}

	.info {
		max-width: 400px;

		& .name {
			display: inline-block;

			color: var(--ft1);
			font-weight: 700;
			font-size: 1.2rem;
			text-decoration: none;

			transition: color 0.2s ease-in-out;
			&:hover {
				color: var(--link-color-hover, color-mix(in srgb, var(--cl1), black 30%));
			}
		}

		& .name,
		& .description {
			margin-top: 16px;
		}

		& .tag {
			margin-top: 16px;
			gap: 4px;
		}
	}
</style>
