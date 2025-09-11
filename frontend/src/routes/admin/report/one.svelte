<script>
	import { module } from '$lib/store.svelte.js';

	let { one } = $props();

	import { Datetime, Avatar } from '$lib/macro';
	import { Link } from '$lib/button';
	import Resolve from './one_resolve.svelte';
</script>

<div class="one">
	<div class="small line gap">
		<!-- <div class="date">
			<Datetime datetime={one.date_created} type="date" />
			<Datetime datetime={one.date_created} type="time" />
		</div> -->
		<span>
			id: <span class="caps"> {one.key.slice(-10)} </span>
		</span>
		<Link small onclick={() => module.open(Resolve, { report_key: one.key })}>Resolve</Link>
	</div>

	<div class="user">
		<Avatar name={one.user.name} photo={one.user.photo} --avatar-border-radius="50%" />
		<div class="details">
			<Link href="/@{one.user.username}" blank>
				{one.user.name}
			</Link>
			<div class="small">
				{one.comment}
				<br />
				{#each one.tags as x}
					#{x}{/each}
			</div>
		</div>
	</div>
	<!-- <div></div> -->
	<!-- <Link href="/{one.entity.extra_2}#{one.entity.key}" blank>
			{one.entity.extra_1}
		</Link> -->

	<br />
	Reported
	<br />
	<br />

	<div class="entity">
		{#if one.entity_type == 'comment'}
			<a href="/{one.comment.post_key}">
				{one.comment.comment}
			</a>
		{:else if one.entity_type == 'user'}
			<div class="user">
				<Avatar
					name={one.reporter_user.name}
					photo={one.reporter_user.photo}
					--avatar-border-radius="50%"
				/>
				<div class="details">
					<Link href="/@{one.reporter_user.username}" blank>
						{one.reporter_user.name}
					</Link>
				</div>
			</div>
		{/if}
	</div>
</div>

<style>
	.one {
		margin: var(--sp2) 0;
		padding-top: var(--sp2);
		border-top: 2px solid var(--input);
	}

	.user {
		display: flex;
		gap: 16px;
	}

	.small {
		font-size: 0.8rem;
		color: var(--ft2);
	}

	.caps {
		text-transform: uppercase;
	}
</style>
