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
	<div class="img">
		<img src={post.photos[0] || '/no_photo.png'} alt={post.title} />
	</div>

	<div class="details">
		<div>
			<div class="title">
				{post.title}
			</div>
			<div class="description">
				{post.description}
			</div>
		</div>
	</div>

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
</a>

<style>
	a {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;

		text-decoration: none;

		border-radius: var(--sp0);
		outline: 2px solid transparent;

		background-color: var(--bg1);
		color: var(--ft2);

		transition: background-color var(--trans), outline-color var(--trans);
	}
	a:hover {
		outline-color: var(--ft2);
	}

	.img {
		overflow: hidden;
		flex-shrink: 0;
	}
	img {
		display: block;

		width: 100%;
		object-fit: cover;
		aspect-ratio: 3 / 2;
		background-color: var(--bg2);

		transition: transform var(--aTime);
		transition-timing-function: ease-in-out;
	}
	a:hover img {
		transform: scale(1.2) rotate(5deg);
	}

	.details {
		display: flex;
		flex-direction: column;
		justify-content: space-between;

		height: 100%;
		padding: 0 var(--sp3);
	}

	.title {
		color: var(--ft1);
		margin: var(--sp2) 0;
		line-height: 120%;
		font-weight: 700;
	}

	.description {
		margin: var(--sp2) 0;
		color: var(--ft1);
		transition: color var(--trans);

		font-size: 0.8rem;
	}

	.bottom {
		font-size: 0.8rem;
		transition: color var(--trans);
		justify-content: space-between;
		flex-wrap: wrap;
		gap: var(--sp2);

		line-height: 1;
		padding: var(--sp1) var(--sp3);
		border-top: 1px solid var(--bg2);
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
