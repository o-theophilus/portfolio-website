<script>
	import { Button, FoldButton, Link } from '$lib/button';
	import { Avatar, Datetime } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import Form from './_form.svelte';

	let { report, update } = $props();
	let open = $state(false);
</script>

<div class="one">
	<div class="user">
		<a href="/@{report.user.username}">
			<Avatar name={report.user.name} photo={report.user.photo} --avatar-border-radius="50%" />
		</a>
		<div class="right">
			<div class="line space">
				<div class="div">
					<a href="/@{report.user.username}" class="name">
						{report.user.name}
					</a>

					<div class="username">
						@{report.user.username}
					</div>
				</div>
				<FoldButton {open} onclick={() => (open = !open)}></FoldButton>
			</div>

			{#if report.entity_type == 'comment'}
				<div class="comment_area_1">
					<div class="line space">
						<div class="date">
							<Datetime datetime={report.user_comment.date_created} type="date_numeric"></Datetime>
							<Datetime datetime={report.user_comment.date_created} type="time_12h"></Datetime>
						</div>

						<Link
							--link-font-size="0.8rem"
							href="/{report.user_comment.post_key}#{report.entity_key}"
						>
							post
						</Link>
					</div>
					<div class="comment">
						{report.user_comment.comment}
					</div>
				</div>
			{/if}
		</div>
	</div>

	{#if open}
		<div class="report" transition:slide>
			<a href="/@{report.reporter.username}">
				<Avatar
					name={report.reporter.name}
					photo={report.reporter.photo}
					--avatar-border-radius="50%"
				/>
			</a>
			<div class="right">
				<a href="/@{report.reporter.username}" class="name">
					{report.reporter.name}
				</a>

				<div class="username">
					@{report.reporter.username}
				</div>

				<div class="comment_area">
					<div class="date">
						<Datetime datetime={report.date_created} type="date_numeric"></Datetime>
						<Datetime datetime={report.date_created} type="time_12h"></Datetime>
					</div>
					<div class="comment">
						{report.comment}
						{#each report.tags as tag}
							&nbsp; #{tag}
						{/each}
					</div>
				</div>

				{#if app.user.access.includes('report:resolve')}
					<Button
						icon="check"
						--button-font-size="0.8rem"
						--button-height="32px"
						onclick={() =>
							module.open(Form, {
								key: report.key,
								entity_type: report.entity_type,
								update
							})}
					>
						Resolve
					</Button>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.one {
		background-color: var(--bg1);

		border-radius: 8px;
		margin: 8px 0;
	}

	.user {
		display: flex;
		gap: 16px;
		padding: 16px;
		align-items: flex-start;
	}
	.right {
		width: 100%;
	}

	.report {
		display: flex;
		gap: 16px;

		padding: 16px;
		border-top: 2px solid var(--bg2);
	}

	.comment_area_1 {
		margin-top: 16px;
	}
	.comment_area {
		margin: 16px 0;
	}
	.name {
		font-weight: 700;
		color: var(--ft1);
	}
	.username {
		font-size: 0.7em;
	}

	.date {
		font-size: 0.7rem;
	}

	a {
		color: var(--ft2);
		text-decoration: none;
	}
</style>
