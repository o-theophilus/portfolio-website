<script>
	import { Icon } from '$lib/macro';

	let { title, data, money, icon, interval } = $props();
</script>

<div class="icon_tv">
	{#if icon}
		<div class="icon">
			<Icon {icon}></Icon>
		</div>
	{/if}

	<div class="tv">
		<div class="title">
			{title}
		</div>

		<div class="value">
			{#if money}
				₦{Number(data.value).toLocaleString()}
			{:else}
				{data?.value}
			{/if}
		</div>
	</div>
</div>

{#if data?.change}
	<div class="change" class:down={data.change < 0}>
		{#if data.change > 0}
			<Icon icon="trending-up"></Icon>
		{:else if data.change < 0}
			<Icon icon="trending-down"></Icon>
		{/if}

		{#if data.change != 0}
			{data.change}%

			{#if data.change > 0}
				increase
			{:else}
				decrease
			{/if}
			from
		{:else}
			same as
		{/if}

		{#if interval == 'today'}
			yesterday
		{:else if interval == '24 hours'}
			the last 24 hours
		{:else if interval == '7 days'}
			last week
		{:else if interval == '1 month'}
			last month
		{/if}
	</div>
{/if}

<style>
	.icon_tv {
		display: flex;
		gap: 8px;

		.icon {
			color: var(--ft1);
			display: flex;
			align-items: center;
			justify-content: center;

			background-color: var(--icon-color, var(--bg2));
			border-radius: 40%;

			width: 40px;
			height: 40px;
			flex-shrink: 0;
		}
	}

	.title {
		font-size: 0.8rem;
	}

	.value {
		font-weight: 800;
		font-size: 1.2rem;
		color: var(--ft1);
	}
	.change {
		font-size: 0.8rem;
		color: green;

		&.down {
			color: red;
		}
	}
</style>
