<script>
	import Icon from '$lib/icon.svelte';
	import One from './exp.one.svelte';

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
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		color: var(--ft1);
		fill: currentColor;
	}

	.title {
		font-weight: 800;
		font-size: 1.1rem;
	}
</style>
