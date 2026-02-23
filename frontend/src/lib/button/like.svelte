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

		color: var(--like-color, hsl(0, 0%, 60%));
		background-color: var(--like-background-color, hsl(0, 0%, 5%));
		outline: 1px solid var(--like-outline-color, light-dark(transparent, hsl(0, 0%, 30%)));
		outline-offset: -1px;
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
		background-color: var(--button-background-color-hover, hsl(0, 0%, 20%));
		color: var(--button-color-hover, hsl(0, 0%, 95%));
		outline-color: var(--button-outline-color-hover, transparent);
	}
	.active {
		background-color: var(--button-background-color-hover, var(--cl1));
	}
</style>
