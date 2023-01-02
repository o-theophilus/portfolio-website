<script>
	import { api_url, is_admin } from '$lib/store.js';

	export let post;
	export let post_type;

	let href = `/${post_type}/${post.slug}`;
	let target = '';
	if (post.format == 'url' && !$is_admin) {
		href = post.content;
		target = '_blank';
	}
</script>

<a {href} {target}>
	<img
		src="{api_url}/{post.photos[0] || ''}"
		alt={post.title}
		onerror="this.src='/site/no_photo.png'"
	/>
	<div class="blocker" />
	<div class="block">
		<strong class="big">
			{post.title}
		</strong>
		<div class="details">
			{#if post.description}
				<br />
				<div class="description">
					{post.description}
				</div>
			{/if}
			<br />
			<div class="date">
				{post.updated_at}
			</div>
		</div>
	</div>
</a>

<style>
	a {
		display: block;

		position: relative;

		height: 300px;

		text-decoration: none;

		border-radius: var(--gap1);
		overflow: hidden;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}

	a:hover .block {
		top: 0;
		background-color: var(--overlay);
	}
	a:hover .details {
		height: initial;
	}
	a:hover strong {
		color: var(--color1);
	}

	img {
		display: block;
		width: 100%;
		height: 100%;

		object-fit: cover;

		background-color: var(--foreground);
	}

	.block {
		position: absolute;

		display: flex;
		flex-direction: column;
		justify-content: center;

		color: var(--light_color);

		inset: 0;
		top: 80%;

		background-color: rgba(0, 0, 0, 0.3);
		text-align: center;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;

		padding: 0 20px;
	}
	.details {
		height: 0;
		overflow: hidden;
	}
	strong {
		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}

	@media screen and (min-width: 500px) {
		.block {
			padding: 0 20%;
		}
	}
	@media screen and (min-width: 600px) {
		a {
			height: 400px;
			line-height: unset;
		}
	}
</style>
