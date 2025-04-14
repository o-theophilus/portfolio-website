<script>
	import { flip } from 'svelte/animate';
	import { fade, fly } from 'svelte/transition';
	import { cubicInOut, cubicOut } from 'svelte/easing';
	import { goto } from '$app/navigation';
	import { module, settings, user, state } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Link from '$lib/button/link.svelte';
	import BRound from '$lib/button/round.svelte';
	import Icon from '$lib/icon.svelte';
	import Edit from './edit.svelte';
	import Tags from '$lib/tags.svelte';

	let list = [];
	let prev = [];
	let next = [];
	let active = {};

	const set = (key, dir = 0) => {
		let index = $settings.highlight.findIndex((x) => x.key == key);
		if (index == -1) {
			index = 0;
		}

		index = index + dir;

		if (index > $settings.highlight.length - 1) {
			index = 0;
		} else if (index < 0) {
			index = $settings.highlight.length - 1;
		}
		active = $settings.highlight[index];

		let right = $settings.highlight.slice(index);
		let left = $settings.highlight.slice(0, index);
		list = [...right, ...left];
		list.shift();

		let split = list.length;
		if (split % 2) {
			split++;
		}
		split = split / 2;

		prev = list.slice(split);
		next = list.slice(0, split);

		let len = 2;
		prev = prev.slice(-len);
		next = next.slice(0, len);

		list = [...prev, active, ...next];
	};

	const get = (key) => {
		let side = 0;
		let zi = 0;

		let index = prev.findIndex((x) => x.key == key);
		if (index != -1) {
			side = -1;
			zi = prev.length - index;
		} else {
			index = next.findIndex((x) => x.key == key);
			if (index != -1) {
				side = 1;
				zi = index + 1;
			}
		}

		return [side, zi];
	};

	const update = () => {
		list = [];
		prev = [];
		next = [];
		active = {};
		if ($settings.highlight.length > 0) {
			active = $settings.highlight[0];
			set(active.key);
		}
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
				<br />

				<dir class="carousel">
					<div class="block">
						{#each list as post (post.key)}
							{@const values = [...get(post.key)]}

							<img
								style:--side={values[0]}
								style:--zi={values[1]}
								animate:flip={{ duration: 500, easing: cubicInOut }}
								in:fade|local={{ delay: 0, duration: 500, easing: cubicInOut }}
								out:fly|local={{
									delay: 0,
									duration: 100,
									easing: cubicOut,
									x: 200 * values[0],
									opacity: 0
								}}
								on:click={() => {
									if (post.key == active.key) {
										goto(`/${active.slug}`);
									} else {
										set(post.key);
									}
								}}
								role="presentation"
								src={post.photo || '/no_photo.png'}
								alt={post.title}
								onerror="this.src='/file_error.png';"
							/>
						{/each}
					</div>
				</dir>

				{#key active.key}
					<div class="info" in:fade|local={{ delay: 0, duration: 500, easing: cubicInOut }}>
						<div class="nav">
							{#if $settings.highlight.length > 1}
								<BRound
									large
									icon="arrow_back"
									on:click={() => {
										set(active.key, -1);
									}}
								/>
							{:else}
								<div />
							{/if}

							<div class="title_one">
								<Link href="/{active.slug}">
									<div class="name">
										{active.title}
									</div>
								</Link>
							</div>

							{#if $settings.highlight.length > 1}
								<BRound
									large
									icon="arrow_forward"
									on:click={() => {
										set(active.key, 1);
									}}
								/>
							{:else}
								<div />
							{/if}
						</div>

						<div class="title_two">
							<Link href="/{active.slug}">
								<div class="name">
									{active.title}
								</div>
							</Link>
						</div>

						{#if active.description}
							<div class="description">
								{active.description}
							</div>
						{/if}
						
						<div class="tags">
							<Tags
								center
								style="1"
								tags={active.tags}
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
					</div>
				{/key}

				<br />

				<Link href="/post">
					<div class="link">
						View more
						<Icon icon="arrow_forward" />
					</div>
				</Link>
			{/if}
		</dir>
	</Content>
{/if}

<style>
	.title {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

	.carousel {
		display: flex;
		align-items: center;
		justify-content: center;

		overflow: hidden;
	}

	.carousel .block {
		position: relative;
		z-index: 0;

		width: 100%;
		max-width: 400px;
		aspect-ratio: 4/3;
	}
	@media screen and (min-width: 600px) {
		.carousel .block {
			width: 60%;
		}
	}

	img {
		--trans1: 0.5s ease-in-out;
		position: absolute;

		width: 100%;
		height: 100%;

		object-fit: cover;
		font-size: 1.5rem;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.449);
		background-color: var(--bg2);
		border-radius: var(--sp1);
		cursor: pointer;
		outline: 2px solid transparent;
		outline-offset: -2px;

		z-index: calc(0 - var(--zi));
		transform: translateX(calc(80px * var(--side) * var(--zi))) scale(calc(1 - 0.15 * var(--zi)));
		transition: transform var(--trans1), background-color var(--trans1), z-index var(--trans1),
			outline-color var(--trans);
	}

	img:hover {
		outline-color: var(--cl1);
	}

	.comp {
		margin: var(--sp5) 0;
	}

	.nav {
		display: flex;
		align-items: flex-start;
		justify-content: center;
		gap: var(--sp2);

		margin-top: var(--sp3);
	}
	.title_one {
		display: none;
	}
	.title_two {
		margin-top: var(--sp2);
	}

	@media screen and (min-width: 300px) {
		.nav {
			justify-content: space-between;
		}
		.title_one {
			display: block;
		}
		.title_two {
			display: none;
		}
	}

	.name {
		text-align: center;
		color: var(--ft1);

		font-weight: 700;
		font-size: 1.2rem;
		transition: color var(--trans);
	}
	.name:hover {
		color: var(--cl1);
	}

	.description {
		margin: var(--sp2) auto;
		transition: grid-template-rows var(--trans), margin var(--trans);
		text-align: center;
	}

	.tags {
		margin: var(--sp2) auto;
	}

	.name,
	.description,
	.tags {
		max-width: 400px;
	}

	.link {
		display: inline-flex;
		align-items: center;
		gap: var(--sp1);
		width: fit-content;
		transition: gap var(--trans);
	}

	.link:hover {
		gap: var(--sp2);
	}
</style>
