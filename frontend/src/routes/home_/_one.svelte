<script>
	import Tag from '$lib/button/tag.svelte';
	import Link from '$lib/button/link.svelte';

	export let post;
</script>

<div class="comp">
	<a class="img" href="/{post.slug}">
		<img src={post.photos[0] || '/no_photo.png'} alt={post.title} />
	</a>

	<div class="details">
		<Link>
			<div class="title">
				{post.title}
			</div>
		</Link>

		<div class="description">
			{post.description}
		</div>

		{#if post.tags.length > 0}
			<div class="tags">
				{#each post.tags as tag}
					<Tag no_grow>
						{tag}
					</Tag>
				{/each}
			</div>
		{/if}
	</div>
</div>

<style>
	.comp {
		display: flex;
		flex-direction: column;
		margin: var(--sp2) 0;
		gap: var(--sp2);

		text-decoration: none;
		color: var(--ft1);

		border-bottom: 1px solid var(--bg2);
	}
	.img {
		display: block;
		max-width: 400px;
	}

	img {
		display: block;
		height: 300px;
		width: 100%;

		border-radius: var(--sp1);
		object-fit: cover;
		background-color: var(--bg2);

		/* transition: transform var(--aTime); */
		/* transition-timing-function: ease-in-out; */
	}

	.title {
		/* margin-top: var(--sp2); */
		color: var(--ft1);
		font-weight: 700;
		font-size: 1.2rem;
		transition: color var(--trans);
	}

	@media screen and (min-width: 600px) {
		.comp {
			flex-direction: unset;
			border: none;
		}

		.img {
			flex-shrink: 0;
			width: 50%;
		}
	}

	.description {
		margin: var(--sp1) 0;
		transition: grid-template-rows var(--trans), margin var(--trans);
	}
	
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
		margin-top: var(--sp1) ;
		margin-bottom: var(--sp2) ;
	}
</style>
