<script>
	import { app } from '$lib/store.svelte.js';

	import { Datetime, Icon } from '$lib/macro';

	let { item } = $props();

	const prerender = () => {
		app.post = item;
	};
	let src = $state(item.photo ? `${item.photo}/500`: '/no_photo.png');
</script>

<a href="/{item.slug}" onclick={prerender} onmouseenter={prerender}>
	<img {src} loading="lazy" alt={item.title} onerror={() => (src = '/file_error.png')} />

	<div class="details">
		<div class="title">
			{item.title}
		</div>

		{#if item.description}
			<div class="description">
				<div>
					{item.description}
				</div>
			</div>
		{/if}

		<div class="bottom line">
			<Datetime datetime={item.date_created} type="ago" />
			<div class="line info">
				<div class="line">
					<Icon icon="eye" size="12" />
					{item.engagement.view}
				</div>

				<div class="line">
					<Icon icon="message-circle" size="12" />
					{item.engagement.comment}
				</div>

				<div class="line">
					<Icon icon="thumbs-up" size="12" />
					{item.engagement.like}
				</div>
			</div>
		</div>
	</div>
</a>

<style>
	a {
		display: block;
		position: relative;
		text-decoration: none;

		outline: 2px solid transparent;
		transition: outline-color var(--trans);

		border-radius: var(--sp0);
		overflow: hidden;
	}

	img {
		display: block;

		width: 100%;
		object-fit: cover;
		aspect-ratio: 3/4;
		background-color: var(--bg1);

		transition: transform var(--aTime);
		transition-timing-function: ease-in-out;
	}

	a:hover {
		outline-color: var(--ft1);
	}
	a:hover img {
		transition-duration: 5s;
		transform: scale(1.2) rotate(5deg);
	}

	a:hover .description {
		grid-template-rows: 1fr;
		margin: var(--sp2) 0;
	}

	.details {
		position: absolute;
		bottom: 0;

		width: 100%;
		padding: 0 var(--sp3);

		color: var(--ft1);
		background-color: color-mix(in srgb, var(--bg1), transparent 10%);
	}

	.title {
		margin: var(--sp2) 0;
		line-height: 120%;
		font-weight: 700;
		transition: color var(--trans);
	}

	.description {
		display: grid;
		grid-template-rows: 0fr;

		color: var(--ft2);
		font-size: 0.8rem;
		transition:
			grid-template-rows var(--trans),
			margin var(--trans);
	}
	.description div {
		overflow-y: hidden;
	}

	.bottom {
		font-size: 0.8rem;
		transition: color var(--trans);
		justify-content: space-between;
		flex-wrap: wrap;
		gap: var(--sp2);

		color: var(--ft2);
		line-height: 1;
		padding: var(--sp1) 0;
		border-top: 1px solid gray;
	}

	.line {
		gap: 0;
	}

	.info {
		gap: 8px;
	}
</style>
