<script>
	import { api_url, _user } from '$lib/store.js';

	export let post;

	let href = `/${post.type}/${post.slug}`;
	let target = '';
	if (post.format == 'url' && !$_user.roles.includes('admin')) {
		href = post.content;
		target = '_blank';
	}
</script>

<a {href} {target} data-sveltekit-preload-data class:draft={post.status == 'draft'}>
	<div class="img">
		<img
			src="{api_url}/{post.photos[0] || ''}"
			alt={post.title}
			onerror="this.src='/site/no_photo.png'"
		/>
	</div>
	<div class="details">
		<strong class="big color1">
			{post.title}
		</strong>
		{#if post.description}
			<br />
			<div class="description">
				{post.description}
			</div>
		{:else}
			<br />
		{/if}
		<br />
		<div class="date">
			{post.created_at.split('T')[0]}
		</div>
	</div>
</a>

<style>
	a {
		padding: var(--gap3);

		background-color: var(--accent5);
		color: var(--accent2);
		text-decoration: none;

		border-radius: var(--gap1);
		border: 2px solid transparent;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	a.draft {
		border: 2px solid var(--color2);
	}
	a:hover {
		border-color: var(--accent2);
	}

	.img {
		border-radius: var(--gap1);
		overflow: hidden;
		
	}
	img {
		display: block;
		/* width: 100%; */
		/* height: 100%; */
		
		object-fit: cover;
		aspect-ratio: 1 / 1;
		background-color: var(--accent4);

		transition: transform var(--animTime3);
		transition-timing-function: ease-in-out;
	}
	a:hover img {
		transform: scale(1.2);
	}

	.details {
		padding-top: var(--gap3);
	}
	strong {
		font-size: large;
		/* color: var(--color1); */
	}
</style>
