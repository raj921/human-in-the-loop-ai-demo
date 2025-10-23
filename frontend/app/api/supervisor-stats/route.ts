import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Return simulated stats directly
    return NextResponse.json({
      pending: 0,
      total: 0,
      resolved: 0,
      learned_answers: 0
    });
  } catch (error) {
    console.error('Error in stats endpoint:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
