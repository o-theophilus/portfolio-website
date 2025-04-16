<script>
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { goto } from '$app/navigation';
	import { module, settings, user, state } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Link from '$lib/button/link.svelte';
	import BRound from '$lib/button/round.svelte';
	import Icon from '$lib/icon.svelte';
	import Edit from './edit.svelte';
	import Tags from '$lib/tags.svelte';

	let index = 0;

	const set = (dir = 0) => {
		index = index + dir;

		if (index > $settings.highlight.length - 1) {
			index = 0;
		} else if (index < 0) {
			index = $settings.highlight.length - 1;
		}
	};

	const update = () => {
		index = 0;
	};

	update();
</script>

{#if $settings.highlight.length > 0 || $user.access.includes('post:edit_highlight')}
	<Content fit>
		<dir class="comp">
			<div class="title">
				<strong class="ititle">
					Some Thing{$settings.highlight.length > 1 ? 's' : ''}
					I've Built
				</strong>

				{#if $user.access.includes('post:edit_highlight')}
					<BRound
						icon="edit"
						on:click={() => {
							$module = {
								module: Edit,
								update
							};
						}}
					/>
				{/if}
			</div>

			{#if $settings.highlight.length > 0}
				<Link href="/post">
					<div class="view_more">
						View more
						<Icon icon="arrow_forward" />
					</div>
				</Link>

				<br />
				<br />

				<dir class="carousel">
					{#key index}
						<img
							in:fade|local={{ delay: 0, duration: 500, easing: cubicInOut }}
							on:click={() => {
								goto(`/${$settings.highlight[index].slug}`);
							}}
							role="presentation"
							src={$settings.highlight[index].photo || '/no_photo.png'}
							alt={$settings.highlight[index].title}
							onerror="this.src='/file_error.png';"
						/>
					{/key}
					<div class="hidden">
						{#each Array($settings.highlight.length) as _, i}
							<img
								src={$settings.highlight[i].photo || '/no_photo.png'}
								alt={$settings.highlight[i].title}
							/>
						{/each}
					</div>

					{#if $settings.highlight.length > 1}
						<div class="nav">
							<button
								on:click={() => {
									set(-1);
								}}
							>
								<Icon icon="arrow_back" />
							</button>

							<button
								on:click={() => {
									set(1);
								}}
							>
								<Icon icon="arrow_forward" />
							</button>
						</div>

						<div class="indicator">
							{#each Array($settings.highlight.length) as _, i}
								<button
									class="one"
									class:active={i == index}
									on:click={() => {
										index = i;
									}}
								/>
							{/each}
						</div>
					{/if}
				</dir>

				{#key index}
					<div class="info" in:fade|local={{ delay: 0, duration: 500, easing: cubicInOut }}>
						<a href="/{$settings.highlight[index].slug}" class="name">
							{$settings.highlight[index].title}
						</a>

						{#if $settings.highlight[index].description}
							<div class="description">
								{$settings.highlight[index].description}
							</div>
						{/if}

						<Tags
							style="1"
							tags={$settings.highlight[index].tags}
							on:click={(e) => {
								let pn = 'post';
								let i = $state.findIndex((x) => x.name == pn);
								if (i != -1) {
									$state.splice(i, 1);
								}

								goto(`post?${new URLSearchParams({ tag: e.detail }).toString()}`);
							}}
						/>
					</div>
				{/key}
			{/if}
		</dir>
	</Content>
{/if}

<style>
	.comp {
		margin: var(--sp5) 0;
	}

	.title {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

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

		display: flex;
		justify-content: space-between;
		pointer-events: none;

		width: calc(100% - var(--sp1) * 2);
	}

	.nav button {
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		border: none;
		width: 40px;
		aspect-ratio: 1/2;
		border-radius: var(--sp0);

		background-color: var(--cld);
		color: var(--clb);
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
		left: 0;

		display: flex;
		gap: var(--gap);
		justify-content: center;

		background-color: var(--cld);
		padding: var(--gap);
		margin: var(--sp1);
		border-radius: calc((var(--size) + var(--size) * 2) / 2);
	}

	.indicator button {
		flex-shrink: 0;
		width: var(--size);
		height: var(--size);

		background-color: var(--clm);
		border-radius: calc(var(--size) / 2);
		border: none;
		cursor: pointer;

		transition: width var(--trans), background-color var(--trans);
	}

	.indicator button.active {
		width: calc(var(--size) * 2);
		background-color: var(--clb);
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

	.view_more {
		display: inline-flex;
		align-items: center;
		gap: var(--sp1);
		width: fit-content;
		transition: gap var(--trans);
	}

	.view_more:hover {
		gap: var(--sp2);
	}
</style>
