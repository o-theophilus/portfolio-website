<script>
	import Icon from '$lib/icon.svelte';
	import One from './skill.one.svelte';

	export let list = [];
	export let name = '';
	export let icon = '';
</script>

<div class="group">
	<div class="line">
		<div class="icon">
			<Icon {icon} size="1.5" />
		</div>
		<div class="title">{name}</div>
	</div>

	{#each list as x}
		<One one={x} />
	{/each}
</div>

<style>
	.group {
		width: 100%;

		padding: var(--sp2);
		border: 2px solid var(--bg2);
		border-radius: var(--sp0);
	}
	.group:hover {
		/* background-color: var(--bg2); */
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		color: var(--ft1);
		fill: currentColor;
	}

	.icon {
		--size: 60px;

		display: flex;
		justify-content: center;
		align-items: center;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);

		background-color: var(--bg2);
		border-radius: var(--sp0);
	}

	.title {
		font-weight: 800;
		font-size: 1.1rem;
	}
</style>
