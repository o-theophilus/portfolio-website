<script>
	import { Icon } from '$lib/macro';

	let { active = '', like = 0, dislike = 0, onlike, ondislike } = $props();
</script>

<div class="group">
	<button class="like" onclick={onlike} class:active={active == 'like'}>
		<Icon icon="thumbs-up" />
		{like}
	</button>

	<button class="dislike" onclick={ondislike} class:active={active == 'dislike'}>
		<Icon icon="thumbs-down" />
		{dislike}
	</button>
</div>

<style>
	.group {
		display: flex;
		align-items: center;
		gap: 1px;
	}

	button {
		display: flex;
		align-items: center;
		gap: 4px;

		height: var(--like-height, 48px);
		padding: 4px 16px;
		font-size: 0.7rem;

		color: var(--like-color, white);
		background-color: var(--like-background-color, var(--cl1));
		outline: 2px solid var(--like-outline-color, light-dark(transparent, hsl(0, 0%, 20%)));
		outline-offset: -2px;
		border: none;
		cursor: pointer;

		transition:
			background-color 0.2s ease-in-out,
			outline-color 0.2s ease-in-out,
			color 0.2s ease-in-out;
	}
	.like {
		border-radius: var(--like-height, 48px) 0 0 var(--like-height, 48px);
	}
	.dislike {
		border-radius: 0 var(--like-height, 48px) var(--like-height, 48px) 0;
	}

	.active,
	button:hover {
		background-color: var(--like-background-color-hover, color-mix(in srgb, var(--cl1), black 30%));
		outline-color: var(--like-outline-color-hover, transparent);
		color: var(--like-color-hover, white);
	}
</style>
