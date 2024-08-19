<script>
	import { state } from '$lib/store.js';

	import Datetime from '$lib/datetime.svelte';
	import Icon from '$lib/icon.svelte';

	export let post;

	const click = () => {
		let sn = 'post_item';
		let i = $state.findIndex((x) => x.name == sn);
		if (i == -1) {
			$state.push({
				name: sn,
				data: post
			});
		} else {
			$state[i].data = post;
		}
	};
</script>

<a href="/{post.slug}" data-sveltekit-preload-data on:click={click} on:mouseenter={click}>
	<img src={post.photos[0] || '/no_photo.png'} alt={post.title} />

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
			<Datetime datetime={post.date} type="ago" />
			<div class="line info">
				<div class="line">
					<Icon icon="visibility" />
					{post.view}
				</div>

				<div class="line">
					<Icon icon="thumb_up" />
					{post._like}
				</div>

				<div class="line">
					<Icon icon="comment" />
					{post.comment}
				</div>
				{#if post.rating > 0}
					<div class="line">
						<Icon icon="hotel_class" />
						{parseFloat(post.rating)}
					</div>
				{/if}
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
		outline-color: var(--clm);
	}
	a:hover img {
		transform: scale(1.2) rotate(5deg);
	}
	/* a:hover .title {
		color: var(--cl1);
	} */
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

		font-size: 0.8rem;
		transition: grid-template-rows var(--trans), margin var(--trans);
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
		border-top: 1px solid var(--clm);
	}

	.line {
		display: flex;
		align-items: center;
		gap: 2px;
	}

	.info {
		gap: var(--sp2);
	}
</style>
