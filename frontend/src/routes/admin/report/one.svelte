<script>
	import { module } from '$lib/store.svelte.js';

	let { one } = $props();

	import { Datetime, Avatar } from '$lib/macro';
	import { Link } from '$lib/button';
	import Resolve from './one_resolve.svelte';
</script>

<div class="item">
	<div class="small line gap">
		<div class="date">
			<Datetime datetime={one.date} type="date" />
			<Datetime datetime={one.date} type="time" />
		</div>
		<span>
			id:
			<span class="caps">
				{one.key.slice(-10)}
			</span>
		</span>
	</div>

	<a href="/@{one.reporter.username}">
		{one.reporter.name}
	</a>
	<div class="small">
		{one.report}{#each one.tags as x}&nbsp; #{x}{/each}
	</div>

	<div class="highlight">
		<Avatar name={one.reported.name} photo={one.reported.photo} --avatar-border-radius="50%" />
		<Link href="/@{one.reported.key}" blank>
			{one.reported.name}
		</Link>
		<div></div>
		<Link href="/{one.entity.extra_2}#{one.entity.key}" blank>
			{one.entity.extra_1}
		</Link>
	</div>

	{#if one.status != 'resolved'}
		<Link small onclick={() => module.open(Resolve, { report_key: one.key })}>Resolve</Link>
	{:else if one.status == 'resolved'}
		<div class="small">
			{one.resolve}
		</div>
	{/if}
</div>

<style>
	.item {
		margin: var(--sp2) 0;
		padding-top: var(--sp2);
		border-top: 2px solid var(--input);

		color: var(--ft2);
	}

	.highlight {
		display: grid;
		grid-template-columns: 1fr 100%;
		gap: 0 var(--sp1);
		align-items: center;

		background-color: var(--bg2);
		padding: var(--sp2);
		border-radius: var(--sp0);
		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		gap: var(--sp2);
	}

	.gap {
		justify-content: space-between;
	}

	.small {
		font-size: 0.8rem;
		color: var(--ft2);
	}

	.caps {
		text-transform: uppercase;
	}
</style>
