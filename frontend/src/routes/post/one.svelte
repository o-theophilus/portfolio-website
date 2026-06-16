<script>
	import { app } from '$lib/store.svelte.js';

	import { Datetime, Icon } from '$lib/macro';

	let { post } = $props();

	const prerender = () => {
		app.post = post;
	};
	let src = $state(post.photo ? `${post.photo}/500` : '/no_photo.png');
</script>

<a href="/{post.slug}" onclick={prerender} onmouseenter={prerender}>
	<img {src} loading="lazy" alt={post.title} onerror={() => (src = '/file_error.png')} />

	<div class="details">
		<div class="title">
			{post.title}
		</div>

		{#if post.description}
			<div class="description">
				<div>
					{post.description}
				</div>
			</div>
		{/if}

		<div class="bottom line">
			<Datetime datetime={post.date_created} type="ago" />
			<div class="line info">
				<div class="line">
					<Icon icon="eye" size="12" />
					{post.engagement.view}
				</div>

				<div class="line">
					<Icon icon="message-circle" size="12" />
					{post.engagement.comment}
				</div>

				<div class="line">
					<Icon icon="thumbs-up" size="12" />
					{post.engagement.like}
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

		outline: 1px solid var(--ol);
		transition: outline-color 0.2s ease-in-out;

		border-radius: 8px;
		overflow: hidden;

		&:hover {
			outline-color: var(--ft1);

			& img {
				transition-duration: 5s;
				transform: scale(1.2) rotate(5deg);
			}

			& .description {
				grid-template-rows: 1fr;
				margin: 16px 0;
			}
		}
	}

	img {
		display: block;

		width: 100%;
		object-fit: cover;
		aspect-ratio: 3/4;
		background-color: var(--bg1);

		transition: transform 1s;
		transition-timing-function: ease-in-out;
	}

	.details {
		position: absolute;
		bottom: 0;

		width: 100%;
		padding: 0 24px;

		color: var(--ft1);
		background-color: color-mix(in srgb, var(--bg3), transparent 10%);

		& .title {
			margin: 16px 0;
			line-height: 120%;
			font-weight: 700;
			transition: color 0.2s ease-in-out;
		}

		& .description {
			display: grid;
			grid-template-rows: 0fr;

			color: var(--ft2);
			font-size: 0.8rem;
			transition:
				grid-template-rows 0.2s ease-in-out,
				margin 0.2s ease-in-out;

			& div {
				overflow-y: hidden;
			}
		}
	}

	.bottom {
		font-size: 0.8rem;
		transition: color 0.2s ease-in-out;
		justify-content: space-between;
		flex-wrap: wrap;
		gap: 16px;

		color: var(--ft2);
		line-height: 1;
		padding: 8px 0;
		border-top: 1px solid gray;
	}

	.line {
		gap: 0;
	}

	.info {
		gap: 8px;
	}
</style>
